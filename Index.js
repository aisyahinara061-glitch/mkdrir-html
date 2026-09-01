function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSheet();
    var data = JSON.parse(e.postData.contents);
    
    sheet.appendRow([
      data.timestamp || new Date().toLocaleString('id-ID'),
      data.nama || '-',
      data.kelas || '-',
      data.makanan || '-',
      data.crush || '-',
      data.gambar || '-'
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Data tersimpan!'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// Buat function buat test
function doGet() {
  return ContentService.createTextOutput('✅ Google Script Aktif!');
}
