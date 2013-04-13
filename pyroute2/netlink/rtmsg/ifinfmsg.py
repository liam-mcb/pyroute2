import struct

from socket import AF_INET
from socket import AF_INET6
from pyroute2.arp import ARPHRD_VALUES
from pyroute2.common import map_namespace
from pyroute2.common import t_hex
from pyroute2.common import t_l2ad
from pyroute2.common import t_asciiz
from pyroute2.common import t_none
from pyroute2.common import t_uint8
from pyroute2.common import t_uint32
from pyroute2.netlink.generic import nlmsg
from pyroute2.netlink.generic import nested


##
# ifinfmsg-specific buffer reading "t_" routines
#
def t_state(buf, length):
    """
    Read 8 bit and return interface state as a string
    """
    return IF_OPER_VALUES[struct.unpack("=B", buf.read(1))[0]][8:]


class t_ifmap(nlmsg):
    """
    Interface map structure. This class can be used in
    the attribute mapping, since nlmsg supports this API.
    """
    fmt = "QQQHBB"
    fields = ("mem_start", "mem_end", "base_addr", "irq", "dma", "port")


class t_ifstats(nlmsg):
    """
    Interface statistics
    """
    fmt = "I" * 23
    fields = ("rx_packets", "tx_packets", "rx_bytes", "tx_bytes",
              "rx_errors", "tx_errors", "rx_dropped", "tx_dropped",
              "multicast", "collisions", "rx_length_errors", "rx_over_errors",
              "rx_crc_errors", "rx_frame_errors", "rx_fifo_errors",
              "rx_missed_errors", "tx_aborted_errors", "tx_carrier_errors",
              "tx_fifo_errors", "tx_heartbeat_errors", "tx_window_errors",
              "rx_compressed", "tx_compressed")


class t_ifstats64(t_ifstats):
    """
    Interface statistics, 64bit version
    """
    fmt = "Q" * 23


IFLA_INFO_UNSPEC = 0
IFLA_INFO_KIND = 1
IFLA_INFO_DATA = 2
IFLA_INFO_XSTATS = 3


class t_ifinfo(nested):
    """
    Parse IFLA_LINKINFO attribute
    """
    attr_map = {IFLA_INFO_UNSPEC:      (t_none,    "none"),
                IFLA_INFO_KIND:        (t_asciiz,  "kind"),
                IFLA_INFO_DATA:        (t_hex,     "data"),
                IFLA_INFO_XSTATS:      (t_hex,     "xstats")}


IPSTATS_MIB_NUM = 0
# frequently written fields in fast path, kept in same cache line
IPSTATS_MIB_INPKTS = 1  # InReceives
IPSTATS_MIB_INOCTETS = 2  # InOctets
IPSTATS_MIB_INDELIVERS = 3  # InDelivers
IPSTATS_MIB_OUTFORWDATAGRAMS = 4  # OutForwDatagrams
IPSTATS_MIB_OUTPKTS = 5  # OutRequests
IPSTATS_MIB_OUTOCTETS = 6  # OutOctets
# other fields
IPSTATS_MIB_INHDRERRORS = 7  # InHdrErrors
IPSTATS_MIB_INTOOBIGERRORS = 8  # InTooBigErrors
IPSTATS_MIB_INNOROUTES = 9  # InNoRoutes
IPSTATS_MIB_INADDRERRORS = 10  # InAddrErrors
IPSTATS_MIB_INUNKNOWNPROTOS = 11  # InUnknownProtos
IPSTATS_MIB_INTRUNCATEDPKTS = 12  # InTruncatedPkts
IPSTATS_MIB_INDISCARDS = 13  # InDiscards
IPSTATS_MIB_OUTDISCARDS = 14  # OutDiscards
IPSTATS_MIB_OUTNOROUTES = 15  # OutNoRoutes
IPSTATS_MIB_REASMTIMEOUT = 16  # ReasmTimeout
IPSTATS_MIB_REASMREQDS = 17  # ReasmReqds
IPSTATS_MIB_REASMOKS = 18  # ReasmOKs
IPSTATS_MIB_REASMFAILS = 19  # ReasmFails
IPSTATS_MIB_FRAGOKS = 20  # FragOKs
IPSTATS_MIB_FRAGFAILS = 21  # FragFails
IPSTATS_MIB_FRAGCREATES = 22  # FragCreates
IPSTATS_MIB_INMCASTPKTS = 23  # InMcastPkts
IPSTATS_MIB_OUTMCASTPKTS = 24  # OutMcastPkts
IPSTATS_MIB_INBCASTPKTS = 25  # InBcastPkts
IPSTATS_MIB_OUTBCASTPKTS = 26  # OutBcastPkts
IPSTATS_MIB_INMCASTOCTETS = 27  # InMcastOctets
IPSTATS_MIB_OUTMCASTOCTETS = 28  # OutMcastOctets
IPSTATS_MIB_INBCASTOCTETS = 29  # InBcastOctets
IPSTATS_MIB_OUTBCASTOCTETS = 30  # OutBcastOctets
(IPSTATS_MIB_NAMES, IPSTATS_MIB_VALUES) = map_namespace("IPSTATS_MIB",
                                                        globals())


class t_ipv6_stats(nlmsg):
    fmt = "I" * len(IPSTATS_MIB_NAMES.keys())
    fields = [i[12:].lower() for i in IPSTATS_MIB_NAMES.keys()]


ICMP6_MIB_NUM = 0
ICMP6_MIB_INMSGS = 1  # InMsgs
ICMP6_MIB_INERRORS = 2  # InErrors
ICMP6_MIB_OUTMSGS = 3  # OutMsgs
ICMP6_MIB_OUTERRORS = 4  # OutErrors
(ICMP6_MIB_NAMES, ICMP6_MIB_VALUES) = map_namespace("ICMP6_MIB",
                                                    globals())


class t_icmp6_stats(nlmsg):
    fmt = "Q" * len(ICMP6_MIB_NAMES.keys())
    fields = [i[10:].lower() for i in ICMP6_MIB_NAMES.keys()]


class t_ipv6_cache_info(nlmsg):
    # ./include/uapi/linux/if_link.h: struct ifla_cacheinfo
    fmt = "I" * 4
    fields = ("max_reasm_len", "tstamp", "reachable_time", "retrans_time")


class t_ipv6_devconf(nlmsg):
    # ./include/uapi/linux/ipv6.h
    # DEVCONF_
    fmt = "I" * 30
    fields = ("forwarding",
              "hop_limit",
              "mtu",
              "accept_ra",
              "accept_redirects",
              "autoconf",
              "dad_transmits",
              "router_solicitations",
              "router_solicitation_interval",
              "router_solicitation_delay",
              "use_tempaddr",
              "temp_valid_lft",
              "temp_prefered_lft",
              "regen_max_retry",
              "max_desync_factor",
              "max_addresses",
              "force_mld_version",
              "accept_ra_defrtr",
              "accept_ra_pinfo",
              "accept_ra_rtr_pref",
              "router_probe_interval",
              "accept_ra_rt_info_max_plen",
              "proxy_ndp",
              "optimistic_dad",
              "accept_source_route",
              "mc_forwarding",
              "disable_ipv6",
              "accept_dad",
              "force_tllao",
              "ndisc_notify")


class t_ipv6_devstats(nlmsg):
    fmt = ""
    fields = ("")


IFLA_INET6_UNSPEC = 0
IFLA_INET6_FLAGS = 1
IFLA_INET6_CONF = 2
IFLA_INET6_STATS = 3
IFLA_INET6_MCAST = 4
IFLA_INET6_CACHEINFO = 5
IFLA_INET6_ICMP6STATS = 6


class t_ipv6_conf(nested):
    # read IFLA_AF_SPEC for IPv6
    # ./net/ipv6/addrconf.c: inet6_fill_ifla6_attrs()
    attr_map = {IFLA_INET6_FLAGS:      (t_uint32,          "flags"),
                IFLA_INET6_CONF:       (t_ipv6_devconf,    "devconf"),
                IFLA_INET6_STATS:      (t_ipv6_stats,      "ipv6 stats"),
                IFLA_INET6_MCAST:      (t_hex,             "mc"),
                IFLA_INET6_CACHEINFO:  (t_ipv6_cache_info, "cache info"),
                IFLA_INET6_ICMP6STATS: (t_icmp6_stats,     "icmp6 stats")}


class t_ipv4_conf(nlmsg):
    fmt = "I" * 26
    #  ./include/linux/inetdevice.h: struct ipv4_devconf
    fields = ("sysctl",
              "forwarding",
              "mc_forwarding",
              "proxy_arp",
              "accept_redirects",
              "secure_redirects",
              "send_redirects",
              "shared_media",
              "rp_filter",
              "accept_source_route",
              "bootp_relay",
              "log_martians",
              "tag",
              "arp_filter",
              "medium_id",
              "disable_xfrm",
              "disable_policy",
              "force_igmp_version",
              "arp_announce",
              "arp_ignore",
              "promote_secondaries",
              "arp_accept",
              "arp_notify",
              "accept_local",
              "src_valid_mark",
              "proxy_arp_pvlan",
              "route_localnet")


class t_af_spec(nested):
    """
    Parse IFLA_AF_SPEC structure
    """
    attr_map = {AF_INET:        (t_ipv4_conf,     "AF_INET"),
                AF_INET6:       (t_ipv6_conf,     "AF_INET6")}


## link attributes
IFLA_UNSPEC = 0
IFLA_ADDRESS = 1
IFLA_BROADCAST = 2
IFLA_IFNAME = 3
IFLA_MTU = 4
IFLA_LINK = 5
IFLA_QDISC = 6
IFLA_STATS = 7
IFLA_COST = 8
IFLA_PRIORITY = 9
IFLA_MASTER = 10
IFLA_WIRELESS = 11  # Wireless Extension event - see iproute2:wireless.h
IFLA_PROTINFO = 12  # Protocol specific information for a link
IFLA_TXQLEN = 13
IFLA_MAP = 14
IFLA_WEIGHT = 15
IFLA_OPERSTATE = 16
IFLA_LINKMODE = 17
IFLA_LINKINFO = 18
IFLA_NET_NS_PID = 19
IFLA_IFALIAS = 20
IFLA_NUM_VF = 21
IFLA_VFINFO_LIST = 22
IFLA_STATS64 = 23
IFLA_VF_PORTS = 24
IFLA_PORT_SELF = 25
IFLA_AF_SPEC = 26
IFLA_GROUP = 27
IFLA_NET_NS_FD = 28
IFLA_EXT_MASK = 29
IFLA_PROMISCUITY = 30
IFLA_NUM_TX_QUEUES = 31
IFLA_NUM_RX_QUEUES = 32

IF_OPER_UNKNOWN = 0
IF_OPER_NOTPRESENT = 1
IF_OPER_DOWN = 2
IF_OPER_LOWERLAYERDOWN = 3
IF_OPER_TESTING = 4
IF_OPER_DORMANT = 5
IF_OPER_UP = 6

(IF_OPER_NAMES, IF_OPER_VALUES) = map_namespace("IF_OPER", globals())


t_ifla_attr = {IFLA_UNSPEC:         (t_none,        "none"),
               IFLA_ADDRESS:        (t_l2ad,        "hwaddr"),
               IFLA_BROADCAST:      (t_l2ad,        "broadcast"),
               IFLA_IFNAME:         (t_asciiz,      "dev"),
               IFLA_MTU:            (t_uint32,      "mtu"),
               IFLA_LINK:           (t_uint32,      "link"),
               IFLA_QDISC:          (t_asciiz,      "qdisc"),
               IFLA_STATS:          (t_ifstats,     "stats"),
               IFLA_MASTER:         (t_uint32,      "master"),
               IFLA_WIRELESS:       (t_hex,         "wireless"),
               IFLA_TXQLEN:         (t_uint32,      "txqlen"),
               IFLA_MAP:            (t_ifmap,       "ifmap"),
               IFLA_OPERSTATE:      (t_state,       "state"),
               IFLA_LINKMODE:       (t_uint8,       "linkmode"),
               IFLA_LINKINFO:       (t_ifinfo,      "linkinfo"),
               IFLA_NUM_VF:         (t_uint32,      "vf number"),
               IFLA_STATS64:        (t_ifstats64,   "stats64"),
               IFLA_AF_SPEC:        (t_af_spec,     "af spec"),
               IFLA_GROUP:          (t_uint32,      "group"),
               IFLA_PROMISCUITY:    (t_uint32,      "promiscuity"),
               IFLA_NUM_TX_QUEUES:  (t_uint32,      "tx queues"),
               IFLA_NUM_RX_QUEUES:  (t_uint32,      "rx queues")}


class ifinfmsg(nlmsg):
    """
    Network interface message
    struct ifinfomsg {
        unsigned char  ifi_family; /* AF_UNSPEC */
        unsigned short ifi_type;   /* Device type */
        int            ifi_index;  /* Interface index */
        unsigned int   ifi_flags;  /* Device flags  */
        unsigned int   ifi_change; /* change mask */
    };
    """
    fmt = "BHiII"
    fields = ("family", "ifi_type", "index", "flags", "change")

    def setup(self):
        self['type'] = 'link'
        self['ifi_type'] = ARPHRD_VALUES[self['ifi_type']][7:]
        self.attr_map = t_ifla_attr
