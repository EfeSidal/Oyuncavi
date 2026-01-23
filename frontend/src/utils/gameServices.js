// Game service detection based on IP ranges and ports
const gameServices = {
    valve: {
        name: 'Valve (Steam)',
        color: 'text-blue-400',
        bgColor: 'bg-blue-500/20',
        ports: [27015, 27016, 27017, 27018, 27019, 27020, 27021, 27030, 27031, 27036, 27037],
        ipRanges: ['162.254.', '208.64.', '205.196.', '103.10.']
    },
    riot: {
        name: 'Riot Games',
        color: 'text-red-400',
        bgColor: 'bg-red-500/20',
        ports: [5000, 5100, 5200, 5223, 5300, 8088, 8393, 8394, 8443],
        ipRanges: ['104.160.', '185.40.', '162.249.', '198.41.']
    },
    blizzard: {
        name: 'Blizzard',
        color: 'text-orange-400',
        bgColor: 'bg-orange-500/20',
        ports: [1119, 1120, 3724, 6112, 6113, 6114],
        ipRanges: ['24.105.', '34.117.', '137.221.', '185.60.']
    },
    epic: {
        name: 'Epic Games',
        color: 'text-purple-400',
        bgColor: 'bg-purple-500/20',
        ports: [7777, 7778, 7779, 7780],
        ipRanges: ['18.188.', '52.15.', '54.']
    },
    discord: {
        name: 'Discord',
        color: 'text-indigo-400',
        bgColor: 'bg-indigo-500/20',
        ports: [443, 50000, 50001, 50002, 50003],
        ipRanges: ['162.159.', '66.22.']
    },
    minecraft: {
        name: 'Minecraft',
        color: 'text-green-400',
        bgColor: 'bg-green-500/20',
        ports: [25565, 25575, 19132, 19133],
        ipRanges: []
    }
}

export function detectGameService(packet) {
    const { dst_ip, dst_port, src_ip, src_port } = packet

    for (const [key, service] of Object.entries(gameServices)) {
        // Check ports
        if (service.ports.includes(dst_port) || service.ports.includes(src_port)) {
            return { key, ...service }
        }

        // Check IP ranges
        for (const range of service.ipRanges) {
            if (dst_ip?.startsWith(range) || src_ip?.startsWith(range)) {
                return { key, ...service }
            }
        }
    }

    // Common ports detection
    if (dst_port === 443 || dst_port === 80) {
        return { key: 'web', name: 'Web/HTTPS', color: 'text-slate-400', bgColor: 'bg-slate-500/20' }
    }
    if (dst_port === 53) {
        return { key: 'dns', name: 'DNS', color: 'text-cyan-400', bgColor: 'bg-cyan-500/20' }
    }
    if (dst_port === 3478 || dst_port === 3479) {
        return { key: 'stun', name: 'STUN/VoIP', color: 'text-yellow-400', bgColor: 'bg-yellow-500/20' }
    }

    return null
}

export function getGameServiceStats(data) {
    const stats = {}

    data.forEach(packet => {
        const service = detectGameService(packet)
        if (service) {
            if (!stats[service.key]) {
                stats[service.key] = { ...service, count: 0 }
            }
            stats[service.key].count++
        }
    })

    return Object.values(stats).sort((a, b) => b.count - a.count)
}

export { gameServices }
