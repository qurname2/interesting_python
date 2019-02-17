import asyncio

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):

    dict_value = {}

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        # print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        from_client = data.decode()
        to_send = ClientServerProtocol.data_handling(from_client)
        if to_send is True:
            self.transport.write(b"ok\n\n")
        elif to_send is False:
            self.transport.write(b"error\nwrong command\n\n")
        else:
            test = '\n'.join(to_send)
            message = bytearray('ok\n{}\n\n'.format(test), 'utf8')
            # print('to_send = ', '\n'.join(to_send))
            self.transport.write(message)

    @staticmethod
    def data_handling(data_client):
        data_client_list = data_client.split()
        if len(data_client_list) < 2:
            return False
        if data_client_list[0] == 'put' and len(data_client_list) == 4:
            val_client = (data_client_list[2], data_client_list[3])

            if data_client_list[1] not in ClientServerProtocol.dict_value.keys():
                ClientServerProtocol.dict_value[data_client_list[1]] = []
            if val_client not in ClientServerProtocol.dict_value[data_client_list[1]]:
                ClientServerProtocol.dict_value[data_client_list[1]].append((data_client_list[2], data_client_list[3]))
            return True

        elif data_client_list[0] == 'get' and len(data_client_list) == 2:
            get_client = []
            if data_client_list[1] == '*':
                for k,v in ClientServerProtocol.dict_value.items():
                    for j in v: 
                        # print(k + ' ' + ' '.join(j))
                        value = k + ' ' + ' '.join(j)
                        get_client.append(value)
                        # print('get_cl*= ',get_client)
                return get_client
            else:
                if data_client_list[1] in ClientServerProtocol.dict_value.keys():
                        for value in ClientServerProtocol.dict_value[data_client_list[1]]:
                            # print(data_client_list[1], ' '.join(value))
                            get_client.append(data_client_list[1] + ' ' + ' '.join(value))
                            # print(get_client)
                        return get_client
                else:
                    return True
        else:
            return False


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)

