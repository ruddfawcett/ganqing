const http = require('http');
const port = 3000;

const hanzi = require('hanzi');

// https://stackoverflow.com/a/38448040/6669540
var params=function(req){
  let q=req.url.split('?'),result={};
  if(q.length>=2){
      q[1].split('&').forEach((item)=>{
           try {
             result[item.split('=')[0]]=item.split('=')[1];
           } catch (e) {
             result[item.split('=')[0]]='';
           }
      })
  }
  return result;
}

const server = http.createServer((req, res) => {
  if (req.url === '/favicon.ico') { return res.writeHead(204); }

    res.setHeader('Content-Type', 'application/json;charset=utf-8');
    res.writeHead(200);

    var rad_61_a = false;
    var rad_61_b = false;
    var rad_61 = false;

    var decomposition = hanzi.decomposeMany(decodeURIComponent(params(req).ch));
    Object.keys(decomposition).forEach(function(key, idx) {
      var components = decomposition[key].components2;

      rad_61_a = !rad_61_a ? components.includes("心") : rad_61_a;
      rad_61_b = !rad_61_b ? components.includes("忄") : rad_61_b;
      rad_61 = rad_61_a && rad_61_b;

      var rad = 0;

      if (rad_61_a) { rad = 1 }
      if (rad_61_b) { rad = 2 }
      if (rad_61) { rad = 3 }

      if (idx == Object.keys(decomposition).length - 1) {
        // res.end(JSON.stringify({
        //   rad_61: rad_61,
        //   rad_61_a: rad_61_a,
        //   rad_61_b: rad_61_b
        // }));

        res.end(JSON.stringify({
          rad: rad
        }));
      }
    });
});

server.listen(port, (err) => {
  hanzi.start();
  console.log(`Listening on ${port}...`)
});
