const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const pino = require('pino');
const axios = require('axios');

const MY_PHONE_NUMBER = "+967783297002";

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    
    // إعدادات البوت ليكون أكثر صموداً مع ضعف الشبكة
    const sock = makeWASocket({
        logger: pino({ level: 'silent' }),
        auth: state,
        browser: ['Chrome', 'Windows', '10.0.0'], // هوية متصفح ثابتة
        connectTimeoutMs: 60000, // زيادة وقت انتظار الاتصال
        keepAliveIntervalMs: 30000, // إبقاء الاتصال حياً
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;
        
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) {
                console.log("فقد الاتصال، جاري المحاولة مرة أخرى...");
                connectToWhatsApp();
            }
        } else if (connection === 'open') {
            console.log('--- متصل بسيرفرات واتساب بنجاح ---');
            
            // طلب كود الربط إذا لم يكن الجهاز مسجلاً
            if (!sock.authState.creds.me) {
                try {
                    const code = await sock.requestPairingCode(MY_PHONE_NUMBER);
                    console.log('=========================================');
                    console.log('كود الربط الخاص بك هو: ' + code);
                    console.log('=========================================');
                } catch (e) {
                    console.log("خطأ في طلب الكود، البوت قد يكون مسجلاً أو الشبكة تحظره.");
                }
            }
        }
    });

    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;
        const msg = messages[0];
        if (!msg.message || msg.key.fromMe) return;
        
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text;
        if (!text) return;

        try {
            // إرسال الرسالة للسيرفر المحلي الخاص بك
            const response = await axios.post('http://localhost:8000/webhook', { message: text });
            await sock.sendMessage(msg.key.remoteJid, { text: response.data.reply });
        } catch (err) {
            console.error("خطأ في الاتصال بسيرفر الذكاء الاصطناعي:", err.message);
        }
    });
}

connectToWhatsApp();

