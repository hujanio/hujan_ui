function ajax(address, data, typeSend, callback) {
    let xhr;
    if (typeof XMLHttpRequest === 'undefined') {
            let versions = ['MSXML2.XmlHttp.5.0', 'MSXML2.XmlHttp.4.0', 'MSXML2.XmlHttp.3.0', 'MSXML2.XmlHttp.2.0', 'Microsoft.XmlHttp'];
            for (let i = 0, len = versions.length; i < len; i++) {
                    try {
                            xhr = new ActiveXObject(versions[i]);
                            break;
                    } catch (e) {}
            }
    } else { xhr = new XMLHttpRequest(); }
    xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && typeof callback === 'function') {
                    try {
                            callback(JSON.parse(xhr.responseText));
                    } catch (e) { callback({ code: xhr.status, message: xhr.statusText }); }
            }
    };
    xhr.open(typeSend, address, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send(data);
}