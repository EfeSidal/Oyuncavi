import { useState, useEffect, useRef, useCallback } from 'react';

const SOCKET_URL = 'ws://localhost:8000/ws';
const RECONNECT_DELAY = 5000; // 5 saniye

/**
 * WebSocket bağlantısını yöneten React Hook
 * @returns {{ isConnected: boolean, lastMessage: any, sendMessage: function }}
 */
export function useGameSocket() {
    const [isConnected, setIsConnected] = useState(false);
    const [lastMessage, setLastMessage] = useState(null);
    const socketRef = useRef(null);
    const reconnectTimeoutRef = useRef(null);

    // Bağlantı kurma fonksiyonu
    const connect = useCallback(() => {
        // Mevcut bağlantı varsa kapat
        if (socketRef.current) {
            socketRef.current.close();
        }

        try {
            const ws = new WebSocket(SOCKET_URL);

            ws.onopen = () => {
                console.log('[WebSocket] Bağlantı kuruldu');
                setIsConnected(true);
                // Reconnect timeout'u temizle
                if (reconnectTimeoutRef.current) {
                    clearTimeout(reconnectTimeoutRef.current);
                    reconnectTimeoutRef.current = null;
                }
            };

            ws.onmessage = (event) => {
                try {
                    // JSON mesaj mı kontrol et
                    const data = JSON.parse(event.data);
                    setLastMessage(data);
                } catch {
                    // JSON değilse raw text olarak kaydet
                    setLastMessage(event.data);
                }
            };

            ws.onclose = () => {
                console.log('[WebSocket] Bağlantı kapandı');
                setIsConnected(false);
                socketRef.current = null;

                // Auto-reconnect: 5 saniye sonra tekrar dene
                console.log(`[WebSocket] ${RECONNECT_DELAY / 1000} saniye sonra yeniden bağlanılacak...`);
                reconnectTimeoutRef.current = setTimeout(() => {
                    connect();
                }, RECONNECT_DELAY);
            };

            ws.onerror = (error) => {
                console.error('[WebSocket] Hata:', error);
            };

            socketRef.current = ws;
        } catch (error) {
            console.error('[WebSocket] Bağlantı hatası:', error);
            // Hata durumunda da reconnect dene
            reconnectTimeoutRef.current = setTimeout(() => {
                connect();
            }, RECONNECT_DELAY);
        }
    }, []);

    // Mesaj gönderme fonksiyonu
    const sendMessage = useCallback((message) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            if (typeof message === 'object') {
                socketRef.current.send(JSON.stringify(message));
            } else {
                socketRef.current.send(message);
            }
        } else {
            console.warn('[WebSocket] Bağlantı açık değil, mesaj gönderilemedi');
        }
    }, []);

    // Component mount olduğunda bağlan
    useEffect(() => {
        connect();

        // Cleanup: Component unmount olduğunda bağlantıyı kapat
        return () => {
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    }, [connect]);

    return {
        isConnected,
        lastMessage,
        sendMessage
    };
}

export default useGameSocket;
