function kirimKeTelegram() {
    const btn = document.getElementById('btnKirim');
    btn.innerHTML = '<span class="loading"></span> MENGIRIM...';
    btn.disabled = true;

    const pesan = `🔥 *RAKYAT JAYA - DATA PEMIMPIN* 🔥\n\n` +
                  `📝 Nama: ${userData.nama}\n` +
                  `🏫 Kelas: ${userData.kelas}\n` +
                  `🍔 Makanan Favorit: ${userData.makanan}\n` +
                  `💕 Suka Sama: ${userData.crush}\n\n` +
                  `🎬 Link Video: https://files.catbox.moe/ix6vj9.mp4\n\n` +
                  `📅 ${new Date().toLocaleString('id-ID')}`;

    fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            chat_id: CHAT_ID,
            text: pesan,
            parse_mode: 'Markdown'
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.ok) {
            showToast('✅ DATA + LINK VIDEO TERKIRIM!');
            btn.innerHTML = '✅ TERKIRIM!';
        } else {
            showToast('❌ GAGAL: ' + data.description);
            btn.innerHTML = '📤 KIRIM KE TELEGRAM';
            btn.disabled = false;
        }
    })
    .catch(err => {
        showToast('❌ ERROR: ' + err.message);
        btn.innerHTML = '📤 KIRIM KE TELEGRAM';
        btn.disabled = false;
    });
                      }
