import socketio

sio = socketio.Client()

@sio.on('connect')
def connect():
    print('io connected')
    

'''class asyncWrapper():
    def __init__(self, sio, authe):
        self.sio = sio
        self.authe = authe

    def start(self):

        t = Thread(target=self.run, name='io', args=())
        t.daemon = True
        t.start()
        return self

    async def run(self):
        await sio.connect('http://localhost:8080', auth = self.authe)
        '''