import bisect


def get_closest_loc_idx(val, gps_data):
    i = bisect.bisect_left(gps_data, val)
    return i


class Callback:
    def run(self, pkt):
        pass


class ProblemScannerCallback(Callback):
    def __init__(self, target_string, gps_data, timestamps):
        self.found_probes = []
        self.target_string = target_string
        self.gps_data = gps_data
        self.timestamps = timestamps

    def run(self, pkt):
        # if is probe request or probe response
        if int(pkt['type']) == 0 and (int(pkt['subtype']) == 4 or int(pkt['subtype']) == 5):
            if self.target_string in pkt['ssid']:
                loc_idx = get_closest_loc_idx(pkt['timestampSeconds'], self.timestamps)
                self.found_probes.append({
                    "rssi": pkt['dbm_signal'],
                    'bssid': pkt['bssid'],
                    'ssid': pkt['ssid'],
                    'location': self.gps_data[loc_idx]
                }
                )


class TargetFinderCallback(Callback):
    def __init__(self, target_list, gps_data, timestamps):
        self.found_targets = []
        self.target_list = target_list
        self.gps_data = gps_data
        self.timestamps = timestamps

    def run(self, pkt):
        macs = [pkt['srcAddr'], pkt['dstAddr'], pkt['transmitterAddr'], pkt['receiverAddr']]
        for m in macs:
            if m in self.target_list:
                loc_idx = get_closest_loc_idx(pkt['timestampSeconds'], self.timestamps)
                self.found_targets.append(
                    {
                        "rssi": pkt['dbm_signal'],
                        'bssid': pkt['bssid'],
                        'ssid': pkt['ssid'],
                        'mac': pkt['srcAddr'],
                        'location': self.gps_data[loc_idx]
                    }
                )
                break


class VendorFinderCallback(Callback):
    def __init__(self, vendors, gps_data, timestamps):
        # vendors is a dict: (vendor, oui)
        self.found_vendors = []
        self.vendors = vendors
        self.gps_data = gps_data
        self.timestamps = timestamps

    def run(self, pkt):
        macs = [pkt['srcAddr'], pkt['dstAddr'], pkt['transmitterAddr'], pkt['receiverAddr']]
        ouis = [m[0:8] for m in macs]
        for oui in ouis:
            for vendor, vendor_addrs in self.vendors.items():
                if oui in vendor_addrs:
                    loc_idx = get_closest_loc_idx(pkt['timestampSeconds'], self.timestamps)
                    self.found_vendors.append(
                        {
                            "rssi": pkt['dbm_signal'],
                            'bssid': pkt['bssid'],
                            'ssid': pkt['ssid'],
                            'mac': pkt['srcAddr'],
                            'vendor': vendor,
                            'location': self.gps_data[loc_idx]
                        }
                    )
                    break


class NetworkAnalyzerCallback(Callback):
    def __init__(self, gps_data, timestamps):
        self.bssid_data = {}
        self.essid_data = {}
        self.ess_list = {}
        self.gps_data = gps_data
        self.timestamps = timestamps

    def run(self, pkt):
        # is beacon
        if pkt['type'] == 0 and pkt['subtype'] == 8:
            loc_idx = get_closest_loc_idx(pkt['timestampSeconds'], self.timestamps)
            data = {
                "rssi": pkt['dbm_signal'],
                'bssid': pkt['bssid'],
                'ssid': pkt['ssid'],
                'location': self.gps_data[loc_idx]
            }
            self.bssid_data.get(pkt['bssid'], []).append(data)
            self.essid_data.get(pkt['ssid'], []).append(data)
            self.ess_list.get(pkt['ssid'], []).append(pkt['bssid'])

