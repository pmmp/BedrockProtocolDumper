from version import Version
from math import ceil
import re
import os

def split_upper(string):
    return filter(None, re.split("([A-Z][^A-Z]*)", string))

def rchop(string, substring):
    if string.endswith(substring):
        return string[:-len(substring)]
    return string

def generate_new_packet_stubs(out, resource_path, packets_dir):
    names = out.values()
    with open(resource_path + 'templates' + os.sep + 'DataPacketTemplate.php') as template_file:
        packet_template = template_file.read()

    # Check existence of old and new packets and create stubs for new stuff
    for i in names:
        if not os.path.exists(packets_dir + i + '.php'):
            print '!!! New packet:', i
            const_name = '_'.join(split_upper(i)).upper()
            base_name = rchop(i, 'Packet')
            with open(packets_dir + i + '.php', 'w') as out_file:
                out_file.write(packet_template % (i, const_name, base_name))

            print 'Created stub class for', i, 'at', (packets_dir + i + '.php')

def check_removed_packets(out, packets_dir):
    names = out.values()
    #Check what old stuff got removed and make noise about it
    class_ignorelist = [
        'BatchPacket',
        'DataPacket',
        'UnknownPacket',
        'PacketPool',
        'Packet',
        'PacketDecodeException',
        'PacketHandlerDefaultImplTrait',
        'PacketHandlerInterface',
        'ClientboundPacket',
        'ServerboundPacket',
        'GarbageServerboundPacket'
    ]
    existing = os.listdir(packets_dir)
    for j in existing:
        if j.endswith('.php'):
            classname = j.split('.php')[0]
            if not 'Packet' in classname or classname in class_ignorelist:
                continue
            if not classname in names:
                print '!!! Removed packet:', classname

def generate_protocol_info(out, version, resource_path, packets_dir):
    with open(resource_path + 'templates' + os.sep + 'ProtocolInfoTemplate.php') as template_file:
        protocol_info_template = template_file.read()

    consts = ''
    last = 0
    for i in out.keys():
        if i != last + 1:
            consts += '\n' #gap in the enum
        last = i
        name = out.get(i)
        if name is None:
            continue
        consts += ('\tpublic const %s = %s;\n' % ('_'.join(split_upper(name)).upper(), format(i, '#04x')))

    with open(packets_dir + 'ProtocolInfo.php', 'w') as out_file:
        out_file.write(protocol_info_template % (version.protocol, str(version.game_version()), str(version.game_version_network()), consts))

    print 'Recreated ProtocolInfo'

def generate_packet_pool(out, resource_path, packets_dir):
    with open(resource_path + 'templates' + os.sep + 'PacketPoolTemplate.php') as template_file:
        pool_template = template_file.read()

    entries = ''
    for i in out.values():
        entries += ('\n\t\t$this->registerPacket(new %s());' % i)

    pool_size = int(ceil(max(out) / 256.0) * 256)
    with open(packets_dir + 'PacketPool.php', 'w') as out_file:
        out_file.write(pool_template % (pool_size, entries))

    print 'Recreated PacketPool'

#PacketHandler
def generate_packet_handler(out, resource_path, packets_dir):
    with open(resource_path + 'templates' + os.sep + 'PacketHandlerDefaultImplTrait.php', 'rb') as template_file:
        packet_handler_template = template_file.read()
    functions = []

    function_template = '\tpublic function handle%s(%s $packet) : bool{\n\t\treturn false;\n\t}'

    for i in out.values():
        base_name = rchop(i, 'Packet')
        functions.append(function_template % (base_name, i))

    with open(packets_dir + os.sep + 'PacketHandlerDefaultImplTrait.php', 'wb') as out_file:
        out_file.write(packet_handler_template % ('\n\n'.join(functions)))

    print 'Recreated packet handler default trait'

#PacketHandler

def generate_packet_handler_interface(out, resource_path, packets_dir):
    with open(resource_path + 'templates' + os.sep + 'PacketHandlerInterfaceTemplate.php', 'rb') as template_file:
        packet_handler_template = template_file.read()
    functions = []

    function_template = '\tpublic function handle%s(%s $packet) : bool;'

    for i in out.values():
        base_name = rchop(i, 'Packet')
        functions.append(function_template % (base_name, i))

    with open(packets_dir + 'PacketHandlerInterface.php', 'wb') as out_file:
        out_file.write(packet_handler_template % ('\n\n'.join(functions)))

    print 'Recreated packet handler interface'

def generate_stuff(out, version, bedrockprotocol_dir):
    resource_path = os.path.dirname(os.path.realpath(__file__)) + os.sep

    if not os.path.exists(bedrockprotocol_dir):
        print 'Directory', bedrockprotocol_dir, 'doesn''t exist, make sure you set the path to your BedrockProtocol installation correctly.'

    packets_dir = os.path.join(bedrockprotocol_dir, 'src') + os.sep
    assert(os.path.exists(packets_dir))
    generate_new_packet_stubs(out, resource_path, packets_dir)
    check_removed_packets(out, packets_dir)
    generate_protocol_info(out, version, resource_path, packets_dir)
    generate_packet_pool(out, resource_path, packets_dir)
    generate_packet_handler(out, resource_path, packets_dir)
    generate_packet_handler_interface(out, resource_path, packets_dir)
    print 'Done'
