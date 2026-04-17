from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Store MAC to port mapping
mac_to_port = {}


# Handle incoming packets
def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.connection.dpid
    in_port = event.port

    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    src = packet.src
    dst = packet.dst

    # Learn source MAC dynamically
    mac_to_port[dpid][src] = in_port
    log.info("Learned %s on port %s", src, in_port)

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]

        # Install forwarding rule
        msg = of.ofp_flow_mod()
        msg.match.dl_dst = dst
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

        log.info("Forwarding %s -> %s", src, dst)

    else:
        out_port = of.OFPP_FLOOD
        log.info("Flooding %s -> %s", src, dst)

    # Send current packet
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.in_port = in_port
    event.connection.send(msg)


# Handle port status changes (host/link down)
def _handle_PortStatus(event):
    dpid = event.connection.dpid
    port_no = event.ofp.desc.port_no

    log.info("Port status changed on switch %s, port %s", dpid, port_no)

    if dpid in mac_to_port:
        remove_list = []

        # Find MAC addresses using this port
        for mac, port in mac_to_port[dpid].items():
            if port == port_no:
                remove_list.append(mac)

        # Remove dead host entries
        for mac in remove_list:
            del mac_to_port[dpid][mac]
            log.info("Removed MAC %s from table", mac)

        # Delete switch flows
        msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
        event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow.addListenerByName("PortStatus", _handle_PortStatus)

    log.info("Dynamic Learning Switch Started")
