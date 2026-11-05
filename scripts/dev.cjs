const {spawn}=require('node:child_process');
const args=process.argv.slice(2);
const read=(key,fallback)=>args.includes(key)?args[args.indexOf(key)+1]:fallback;
const server=spawn('python3',['-m','http.server',read('--port','3000'),'--bind',read('--host','127.0.0.1')],{stdio:'inherit'});
for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>server.kill(signal));
server.on('exit',code=>process.exit(code||0));
