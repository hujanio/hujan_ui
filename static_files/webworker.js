let timeMachine;
importScripts('./ajax.js')
function reqLastMachine(address) {
    ajax(address, null, 'GET',function(f) {
        self.postMessage({ cmd: 'resLastStatusMachine', val: f.data});
        timeMachine = setTimeout(function() { reqLastMachine(address) },10000) 
    });
}

self.addEventListener('message', function (a) {
    let b = a.data;
    switch (b.cmd) {
        case 'endLastStatusMachine':
            clearTimeout(timeMachine);
            break;
        case 'reqLastMachine':
            reqLastMachine(b.val)
        default:
            break;
    }
})