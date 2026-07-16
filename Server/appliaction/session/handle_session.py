class SessionHandler():
    def start(server, client_session):
        while True:
            conn, addr = server.accept()
            ddr = addr[0]+":"+str(addr[1])

            print("Connection recv: ", ddr)

            client_session.insert_client(ddr, conn)