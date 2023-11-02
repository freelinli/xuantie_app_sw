#!/usr/bin/env python3

class UsrProtocol:
    property_id = {
            "Error": 0x0,
            "GPS": 0x1,
            "Temperature": 0x2,
            "Speed": 0x3,
            "HW_Status": 0x4,
            "Battery_Power": 0x5,
            "Version": 0x6,
            "WIFI": 0x7,
            "CLI": 0x8,
            "Upgrade": 0x9,
        }
    def __init__(self):
        self.header_link_mode = ("4G", "WIFI", "CABLE", "CLOUD")
        self.secure = ("No", "Yes")
        pass
    def msg_invalid_check(self, arrary_in):
        arrary_out = [0]
        return arrary_out
    def msg_debug(self, arrary_in):
        print("header secure:\t{0:s}".format(self.secure[(arrary_in[0] & 0x80) >> 7]))
        print("header:\t{0:s}".format(self.header_link_mode[arrary_in[0]&0x3]))
        print("seq:\t{0:d}".format(arrary_in[1]))
        print("device id:\t{0}".format(arrary_in[2:6]))
        print("property id:\t{0}".format(arrary_in[6]))
        print("length:\t{0}".format(arrary_in[7]))
        print("data:\t{0}".format(arrary_in[8:-1]))
        print("crc:\t{0}".format(arrary_in[-1:]))
        print("================================")

    def client_service(self, arrary_in):
        arrary_out = [0]
        print("property id:\t{0}".format(arrary_in[6]))
        return arrary_out

    def server_service(self, arrary_in):
        arrary_out = [0]
        return arrary_out
    def server_get(self, address, property):
        arrary_out = [0x00, 0x0f, 0xaa, 0xaa, 0xaa, 0xaa, 0x1, 0x1, 0x8, 0x10]
        arrary_out[2:6] = address
        arrary_out[6] = property
        arrary_out[9] = sum(arrary_out[0:9])
        return arrary_out
    def server_set(self, property, data_array):
        arrary_out = [0]
        return arrary_out

if __name__ == "__main__":
    protocol = UsrProtocol()
    protocol.msg_debug([0x80, 0x0f, 0xaa, 0xaa, 0xaa, 0xaa, 0x1, 0x1, 0x8, 0x10])
    protocol.msg_debug([0x0, 0x10, 0xaa, 0xaa, 0xaa, 0xaa, 0x1, 0x3, 0x08, 0x18, 0x28, 0x10])
    gps_get = protocol.server_get([0x1, 0x2, 0x3, 0x4], protocol.property_id["Upgrade"])
    protocol.msg_debug(gps_get)
    protocol.client_service(gps_get)