let isPairingRequested = false;
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const pino = require('pino');
const axios = require('axios');

// رقمك مضاف هنا كما طلبت
const MY_PHONE_NUMBER = "967783297002"; 

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');

    const sock = makeWASocket({
        logger: pino({ level: 'silent' }),
        auth: state,
        browser: ['Chrome', 'Windows', '10.0.0'],
        connectTimeoutMs: 60000,
        keepAliveIntervalMs: 30000,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    // منطق إظهار كود الربط
    if (!sock.authState.creds.registered) {
        setTimeout(async () => {
            try {
                const phoneNumber = MY_PHONE_NUMBER.replace(/[^0-9]/g, '');
        isPairingRequested = true;
        console.log("جارٍ طلب كود الربط...");
        try {
            const code = await sock.requestPairingCode("967783297002");
            console.log("✅ كود الربط الخاص بك هو: " + code);
        } catch (error) {
            console.error("خطأ أثناء طلب الكود:", error);
            isPairingRequested = false;
        }
                console.log("------------------------------------------");
                console.log("✅ كود الربط الخاص بك هو: " + code);
                console.log("------------------------------------------");
            } catch (error) {
                console.error("خطأ في توليد كود الربط:", error);
            }
        }, 5000); 
    }

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) {
                connectToWhatsApp();
            }
        } else if (connection === 'open') {
            console.log('✅ تم الاتصال بالواتساب بنجاح!');
        }
    });
}

connectToWhatsApp();

