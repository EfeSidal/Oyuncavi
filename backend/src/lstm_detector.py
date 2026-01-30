"""
LSTM Anomaly Detection Module for Network Traffic Analysis.

This module provides an LSTM-based autoencoder for detecting timing anomalies
in network traffic that may indicate speedhack or lag switch cheats.

Features analyzed:
- IAT (Inter-Arrival Time): Time between consecutive packets
- Jitter: Standard deviation of IAT (rhythm irregularity)
- rolling_mean_len: Rolling average of packet lengths
- length: Packet size
- protocol: Network protocol (TCP=6, UDP=17)

Output: Suspicion score (0.0 - 1.0) for each packet sequence
Traffic type classification: game, background, browser, idle
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Tuple, List, Optional
import warnings

# TensorFlow imports with error handling
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed, Input
    from tensorflow.keras.callbacks import EarlyStopping
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    warnings.warn("TensorFlow not installed. LSTM detection will not be available.")


class TrafficProfileGenerator:
    """
    Generate synthetic traffic profiles for LSTM training.
    
    Creates realistic baseline patterns for different traffic types:
    - Game traffic: Low latency, consistent timing, UDP-heavy
    - OS background: Sporadic bursts, Windows Update, telemetry
    - Browser streams: HTTP/2, WebSocket, variable sizes
    - Idle traffic: Minimal activity, keep-alives
    """
    
    # Traffic profile parameters (mean, std) for each metric
    PROFILES = {
        'game': {
            'iat': (0.025, 0.010),        # 25ms ± 10ms (fast, consistent)
            'jitter': (0.005, 0.002),     # Low jitter
            'length': (200, 100),          # 200 bytes ± 100
            'rolling_mean_len': (200, 50),
            'protocol': 17,                # UDP
        },
        'background': {
            'iat': (2.0, 1.5),             # 2s ± 1.5s (sporadic)
            'jitter': (0.5, 0.3),          # High jitter
            'length': (800, 400),          # Larger packets
            'rolling_mean_len': (800, 200),
            'protocol': 6,                 # TCP
        },
        'browser': {
            'iat': (0.1, 0.08),            # 100ms ± 80ms
            'jitter': (0.03, 0.02),        # Medium jitter
            'length': (600, 400),          # Variable sizes
            'rolling_mean_len': (600, 150),
            'protocol': 6,                 # TCP
        },
        'idle': {
            'iat': (5.0, 3.0),             # 5s ± 3s (very slow)
            'jitter': (1.0, 0.5),          # Variable jitter
            'length': (100, 50),           # Small packets
            'rolling_mean_len': (100, 30),
            'protocol': 6,                 # TCP (keep-alives)
        },
    }
    
    @classmethod
    def generate_profile(cls, profile_name: str, n_samples: int = 100) -> pd.DataFrame:
        """
        Generate synthetic traffic data for a given profile.
        
        Args:
            profile_name: One of 'game', 'background', 'browser', 'idle'
            n_samples: Number of packets to generate
            
        Returns:
            DataFrame with synthetic traffic features
        """
        if profile_name not in cls.PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}. Use: {list(cls.PROFILES.keys())}")
        
        profile = cls.PROFILES[profile_name]
        
        # Generate features with realistic distributions
        data = {
            'iat': np.abs(np.random.normal(profile['iat'][0], profile['iat'][1], n_samples)),
            'jitter': np.abs(np.random.normal(profile['jitter'][0], profile['jitter'][1], n_samples)),
            'length': np.clip(np.random.normal(profile['length'][0], profile['length'][1], n_samples), 50, 1500).astype(int),
            'rolling_mean_len': np.clip(np.random.normal(profile['rolling_mean_len'][0], profile['rolling_mean_len'][1], n_samples), 50, 1500),
            'protocol': np.full(n_samples, profile['protocol']),
            'traffic_type': profile_name,
        }
        
        return pd.DataFrame(data)
    
    @classmethod
    def generate_mixed_baseline(cls, samples_per_profile: int = 100) -> pd.DataFrame:
        """
        Generate a mixed baseline of all normal traffic types.
        
        Args:
            samples_per_profile: Number of samples for each traffic type
            
        Returns:
            DataFrame with mixed normal traffic (game, background, browser, idle)
        """
        dfs = []
        for profile_name in cls.PROFILES.keys():
            df = cls.generate_profile(profile_name, samples_per_profile)
            dfs.append(df)
        
        return pd.concat(dfs, ignore_index=True)
    
    @classmethod
    def generate_anomaly_patterns(cls, n_samples: int = 50) -> pd.DataFrame:
        """
        Generate synthetic anomaly patterns (speedhack, lag switch).
        
        Args:
            n_samples: Number of anomaly samples to generate
            
        Returns:
            DataFrame with anomaly patterns
        """
        anomalies = []
        
        # Speedhack pattern: Unnaturally fast and consistent
        speedhack = {
            'iat': np.abs(np.random.normal(0.001, 0.0005, n_samples // 2)),  # 1ms (too fast)
            'jitter': np.abs(np.random.normal(0.0001, 0.00005, n_samples // 2)),  # Almost zero jitter
            'length': np.clip(np.random.normal(150, 30, n_samples // 2), 50, 300).astype(int),
            'rolling_mean_len': np.clip(np.random.normal(150, 20, n_samples // 2), 50, 300),
            'protocol': np.full(n_samples // 2, 17),
            'traffic_type': 'anomaly_speedhack',
        }
        anomalies.append(pd.DataFrame(speedhack))
        
        # Lag switch pattern: Long pause followed by burst
        lag_switch_iat = []
        for _ in range(n_samples // 2):
            if np.random.random() < 0.3:  # 30% chance of lag spike
                lag_switch_iat.append(np.random.uniform(2.0, 5.0))  # Long pause
            else:
                lag_switch_iat.append(np.random.uniform(0.001, 0.01))  # Burst
        
        lag_switch = {
            'iat': np.array(lag_switch_iat),
            'jitter': np.abs(np.random.normal(2.0, 1.0, n_samples // 2)),  # Extreme jitter
            'length': np.clip(np.random.normal(200, 100, n_samples // 2), 50, 500).astype(int),
            'rolling_mean_len': np.clip(np.random.normal(200, 100, n_samples // 2), 50, 500),
            'protocol': np.full(n_samples // 2, 17),
            'traffic_type': 'anomaly_lagswitch',
        }
        anomalies.append(pd.DataFrame(lag_switch))
        
        return pd.concat(anomalies, ignore_index=True)



class LSTMDetector:
    """
    LSTM Autoencoder-based anomaly detector for network traffic.
    
    Uses reconstruction error to identify abnormal packet timing patterns
    that may indicate speedhack or lag switch manipulation.
    
    Supports training on diverse traffic types:
    - Game traffic (low latency, consistent)
    - OS background (sporadic, high latency)
    - Browser streams (medium latency, variable)
    - Idle traffic (minimal activity)
    """
    
    # Extended feature columns (includes length for traffic type classification)
    FEATURES = ['iat', 'jitter', 'rolling_mean_len']
    EXTENDED_FEATURES = ['iat', 'jitter', 'rolling_mean_len', 'length']
    
    def __init__(self, sequence_length: int = 20, threshold: float = 0.7):
        """
        Initialize the LSTM Detector.
        
        Args:
            sequence_length: Number of packets in each sequence (sliding window size)
            threshold: Suspicion score threshold for anomaly classification (0.0 - 1.0)
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for LSTM detection. Install with: pip install tensorflow>=2.10.0")
        
        self.sequence_length = sequence_length
        self.threshold = threshold
        self.model = None
        self.scaler = StandardScaler()
        self._is_trained = False
        
    def _build_model(self, n_features: int) -> Model:
        """
        Build the LSTM Autoencoder model.
        
        Architecture:
        - Encoder: 2 LSTM layers (64 -> 32 units) compress sequence to latent space
        - Decoder: 2 LSTM layers (32 -> 64 units) reconstruct original sequence
        
        Args:
            n_features: Number of input features per timestep
            
        Returns:
            Compiled Keras model
        """
        model = Sequential([
            # Encoder
            LSTM(64, activation='relu', 
                 input_shape=(self.sequence_length, n_features), 
                 return_sequences=True,
                 name='encoder_lstm_1'),
            LSTM(32, activation='relu', 
                 return_sequences=False,
                 name='encoder_lstm_2'),
            
            # Latent space expansion
            RepeatVector(self.sequence_length, name='latent_repeat'),
            
            # Decoder
            LSTM(32, activation='relu', 
                 return_sequences=True,
                 name='decoder_lstm_1'),
            LSTM(64, activation='relu', 
                 return_sequences=True,
                 name='decoder_lstm_2'),
            
            # Output layer
            TimeDistributed(Dense(n_features), name='output')
        ])
        
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def _create_sequences(self, data: np.ndarray) -> np.ndarray:
        """
        Create sliding window sequences from feature data.
        
        Args:
            data: 2D array of shape (n_samples, n_features)
            
        Returns:
            3D array of shape (n_sequences, sequence_length, n_features)
        """
        sequences = []
        for i in range(len(data) - self.sequence_length + 1):
            sequences.append(data[i:i + self.sequence_length])
        return np.array(sequences)
    
    def _preprocess(self, df: pd.DataFrame, fit_scaler: bool = False) -> np.ndarray:
        """
        Extract and normalize features from DataFrame.
        
        Args:
            df: DataFrame with required feature columns
            fit_scaler: Whether to fit the scaler (True for training)
            
        Returns:
            Normalized feature array
        """
        # Validate required columns
        missing_cols = [col for col in self.FEATURES if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Extract features
        features = df[self.FEATURES].values.astype(np.float32)
        
        # Handle NaN/Inf values
        features = np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Normalize
        if fit_scaler:
            features = self.scaler.fit_transform(features)
        else:
            features = self.scaler.transform(features)
            
        return features
    
    def train(self, df: pd.DataFrame, epochs: int = 50, batch_size: int = 32, 
              validation_split: float = 0.1, verbose: int = 0) -> dict:
        """
        Train the LSTM Autoencoder on normal traffic data.
        
        The model learns to reconstruct normal packet timing patterns.
        Anomalies will have higher reconstruction error.
        
        Args:
            df: DataFrame with training data (assumed to be mostly normal traffic)
            epochs: Maximum training epochs
            batch_size: Training batch size
            validation_split: Fraction of data for validation
            verbose: Keras verbosity (0=silent, 1=progress, 2=minimal)
            
        Returns:
            Training history dict
        """
        # Preprocess and create sequences
        features = self._preprocess(df, fit_scaler=True)
        sequences = self._create_sequences(features)
        
        if len(sequences) < 10:
            raise ValueError(f"Not enough data for training. Need at least {self.sequence_length + 9} packets.")
        
        # Build model
        n_features = len(self.FEATURES)
        self.model = self._build_model(n_features)
        
        # Early stopping to prevent overfitting
        early_stop = EarlyStopping(
            monitor='val_loss', 
            patience=5, 
            restore_best_weights=True,
            min_delta=0.001
        )
        
        # Train (autoencoder: input = target)
        history = self.model.fit(
            sequences, sequences,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stop],
            verbose=verbose
        )
        
        self._is_trained = True
        return history.history
    
    def train_with_profiles(self, df: pd.DataFrame = None, 
                            samples_per_profile: int = 200,
                            epochs: int = 50, batch_size: int = 32,
                            validation_split: float = 0.1, verbose: int = 0) -> dict:
        """
        Train on mixed traffic profiles for better traffic type discrimination.
        
        Combines synthetic baseline profiles (game, background, browser, idle)
        with real captured data (if provided) to create a robust training set.
        
        Args:
            df: Optional DataFrame with real captured data to include
            samples_per_profile: Number of synthetic samples per traffic type
            epochs: Maximum training epochs
            batch_size: Training batch size
            validation_split: Fraction of data for validation
            verbose: Keras verbosity
            
        Returns:
            Training history dict
        """
        # Generate synthetic baseline data
        synthetic_df = TrafficProfileGenerator.generate_mixed_baseline(samples_per_profile)
        
        # Combine with real data if provided
        if df is not None and not df.empty:
            # Ensure real data has required columns
            real_df = df.copy()
            real_df['traffic_type'] = 'captured'
            
            # Only use common features
            common_cols = [c for c in self.FEATURES if c in real_df.columns]
            if 'traffic_type' not in common_cols:
                common_cols.append('traffic_type')
            
            # Add missing features with defaults
            for feat in self.FEATURES:
                if feat not in synthetic_df.columns:
                    synthetic_df[feat] = 0
                if feat not in real_df.columns:
                    real_df[feat] = 0
            
            training_df = pd.concat([synthetic_df[self.FEATURES], real_df[self.FEATURES]], ignore_index=True)
        else:
            training_df = synthetic_df[self.FEATURES]
        
        # Shuffle the data
        training_df = training_df.sample(frac=1).reset_index(drop=True)
        
        print(f"[*] Training on {len(training_df)} samples (synthetic + captured)")
        
        # Use the standard train method
        return self.train(training_df, epochs=epochs, batch_size=batch_size,
                         validation_split=validation_split, verbose=verbose)
    
    def classify_traffic_type(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Classify traffic sequences into types based on feature patterns.
        
        Uses simple heuristics based on IAT and packet size to categorize traffic:
        - game: Low IAT (< 100ms), medium packet size
        - background: High IAT (> 500ms), variable size
        - browser: Medium IAT, larger packets
        - idle: Very high IAT, small packets
        
        Args:
            df: DataFrame with traffic features
            
        Returns:
            DataFrame with 'traffic_type' and 'is_game_traffic' columns
        """
        df = df.copy()
        
        # Initialize columns
        df['traffic_type'] = 'unknown'
        df['is_game_traffic'] = False
        
        if 'iat' not in df.columns:
            return df
        
        # Classify based on IAT and packet patterns
        # Game traffic: Low IAT, consistent timing
        game_mask = (df['iat'] < 0.1) & (df['iat'] > 0)
        if 'jitter' in df.columns:
            game_mask &= (df['jitter'] < 0.05)
        df.loc[game_mask, 'traffic_type'] = 'game'
        df.loc[game_mask, 'is_game_traffic'] = True
        
        # Background traffic: High IAT
        background_mask = df['iat'] > 0.5
        df.loc[background_mask, 'traffic_type'] = 'background'
        
        # Idle traffic: Very high IAT, small packets
        idle_mask = df['iat'] > 2.0
        if 'length' in df.columns:
            idle_mask &= (df['length'] < 200)
        df.loc[idle_mask, 'traffic_type'] = 'idle'
        
        # Browser traffic: Medium IAT, larger packets
        browser_mask = (df['iat'] >= 0.05) & (df['iat'] <= 0.5)
        if 'length' in df.columns:
            browser_mask &= (df['length'] > 400)
        df.loc[browser_mask, 'traffic_type'] = 'browser'
        
        return df

    
    def calculate_reconstruction_error(self, sequences: np.ndarray) -> np.ndarray:
        """
        Calculate reconstruction error for each sequence.
        
        Args:
            sequences: 3D array of shape (n_sequences, sequence_length, n_features)
            
        Returns:
            1D array of reconstruction errors (MSE per sequence)
        """
        if self.model is None:
            raise RuntimeError("Model not trained. Call train() first.")
        
        # Get reconstructions
        reconstructed = self.model.predict(sequences, verbose=0)
        
        # Calculate MSE per sequence
        mse = np.mean(np.power(sequences - reconstructed, 2), axis=(1, 2))
        return mse
    
    def _normalize_scores(self, errors: np.ndarray) -> np.ndarray:
        """
        Normalize reconstruction errors to suspicion scores (0.0 - 1.0).
        
        Uses percentile-based normalization:
        - Median error → 0.3 score
        - 95th percentile → 0.8 score
        - Higher errors scale proportionally
        
        Args:
            errors: Array of reconstruction errors
            
        Returns:
            Array of suspicion scores (0.0 - 1.0)
        """
        if len(errors) == 0:
            return np.array([])
        
        # Calculate reference points
        median_err = np.median(errors)
        p95_err = np.percentile(errors, 95)
        
        # Avoid division by zero
        if p95_err <= median_err:
            # All errors are similar, use simple normalization
            max_err = np.max(errors)
            if max_err > 0:
                return np.clip(errors / max_err * 0.5, 0, 1)
            return np.zeros_like(errors)
        
        # Piecewise linear normalization
        scores = np.zeros_like(errors)
        
        # Below median: 0.0 - 0.3
        mask_low = errors <= median_err
        if median_err > 0:
            scores[mask_low] = (errors[mask_low] / median_err) * 0.3
        
        # Median to 95th percentile: 0.3 - 0.8
        mask_mid = (errors > median_err) & (errors <= p95_err)
        scores[mask_mid] = 0.3 + ((errors[mask_mid] - median_err) / (p95_err - median_err)) * 0.5
        
        # Above 95th percentile: 0.8 - 1.0
        mask_high = errors > p95_err
        scores[mask_high] = 0.8 + np.tanh((errors[mask_high] - p95_err) / p95_err) * 0.2
        
        return np.clip(scores, 0, 1)
    
    def detect(self, df: pd.DataFrame, train_first: bool = True) -> pd.DataFrame:
        """
        Detect anomalies in network traffic data.
        
        Args:
            df: DataFrame with packet data including required features
            train_first: If True and model not trained, train on this data first
            
        Returns:
            DataFrame with added 'suspicion_score' and 'lstm_anomaly' columns
        """
        df = df.copy()
        
        # Initialize output columns
        df['suspicion_score'] = 0.0
        df['lstm_anomaly'] = 0
        
        if len(df) < self.sequence_length:
            warnings.warn(f"Not enough packets for analysis. Need at least {self.sequence_length} packets.")
            return df
        
        # Train if needed
        if train_first and not self._is_trained:
            try:
                self.train(df, verbose=0)
            except Exception as e:
                warnings.warn(f"Training failed: {e}. Returning data without LSTM analysis.")
                return df
        
        # Preprocess
        try:
            features = self._preprocess(df, fit_scaler=False)
        except Exception as e:
            warnings.warn(f"Preprocessing failed: {e}")
            return df
        
        sequences = self._create_sequences(features)
        
        if len(sequences) == 0:
            return df
        
        # Calculate reconstruction errors
        errors = self.calculate_reconstruction_error(sequences)
        
        # Normalize to suspicion scores
        scores = self._normalize_scores(errors)
        
        # Map scores back to original DataFrame
        # Each sequence corresponds to packets [i : i + sequence_length]
        # Assign score to the LAST packet in each sequence
        score_indices = range(self.sequence_length - 1, len(df))
        
        for i, score in enumerate(scores):
            if i < len(score_indices):
                idx = df.index[score_indices[i]]
                df.loc[idx, 'suspicion_score'] = float(score)
                df.loc[idx, 'lstm_anomaly'] = 1 if score >= self.threshold else 0
        
        return df


def detect_anomalies_lstm(pcap_file: str, sequence_length: int = 20, 
                          threshold: float = 0.7) -> pd.DataFrame:
    """
    Convenience function for LSTM-based anomaly detection.
    
    This is a drop-in alternative to detect_anomalies() from analysis.py
    that uses LSTM instead of Isolation Forest.
    
    Args:
        pcap_file: Path to PCAP file
        sequence_length: Number of packets per analysis window
        threshold: Suspicion score threshold for anomaly classification
        
    Returns:
        DataFrame with 'suspicion_score' and 'lstm_anomaly' columns,
        or None if analysis failed
    """
    # Import here to avoid circular imports
    from src.analysis import extract_features
    
    df = extract_features(pcap_file)
    
    if df is None or df.empty:
        return None
    
    detector = LSTMDetector(sequence_length=sequence_length, threshold=threshold)
    result_df = detector.detect(df, train_first=True)
    
    return result_df
