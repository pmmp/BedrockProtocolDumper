# BedrockProtocolDumper

## DEPRECATED
This tool has been deprecated due to being inconvenient to use in a multi-developer workflow, and being too restricted.

Please use the improved version of `protocol_info_dumper.py` in [bds-modding-devkit](https://github.com/pmmp/bds-modding-devkit) instead.
The new version generates JSON output instead of PHP code, making it usable for any project.

The new version is located in the devkit for convenience, since the other tools in that repo are typically needed for version updates too, and it makes more sense to have everything in one place.

Generate basic information about new protocol versions from BDS using Python and GNU objdump

## Requirements
- `sudo apt install binutils`
- `python2`
- A local clone of [BedrockProtocol](https://github.com/pmmp/BedrockProtocol)
- An x86_64 Linux binary of [Bedrock Dedicated Server](https://minecraft.net/download/server/bedrock)

## Usage
`python2 protocol_info_generator_objdump.py <path to bedrock_server_symbols.debug> <path to BedrockProtocol src>`

## How does it work?
`protocol_info_generator_objdump` uses [GNU objdump](https://en.wikipedia.org/wiki/Objdump) to extract basic protocol information about a new version of Minecraft from [Bedrock Dedicated Server](https://minecraft.net/download/server/bedrock), including the following:
- Current version (major.minor.patch)
- Whether or not this version is a beta
- Current protocol version
- List of packet IDs

The script currently patches the following files:
- [`ProtocolInfo`](https://github.com/pmmp/BedrockProtocol/blob/a6ccf863a858caa0cf0a322433f8a17d14ee640a/src/ProtocolInfo.php)
- [`PacketPool`](https://github.com/pmmp/BedrockProtocol/blob/a6ccf863a858caa0cf0a322433f8a17d14ee640a/src/PacketPool.php)
- [`PacketHandlerInterface`](https://github.com/pmmp/BedrockProtocol/blob/a6ccf863a858caa0cf0a322433f8a17d14ee640a/src/PacketHandlerInterface.php)
- [`PacketHandlerDefaultImplTrait`](https://github.com/pmmp/BedrockProtocol/blob/a6ccf863a858caa0cf0a322433f8a17d14ee640a/src/PacketHandlerDefaultImplTrait.php)

It will also generate stub classes for any new packets found.

## FAQ
### Can this find packet fields automatically?
No. It can only find some basic information like packet IDs and their associated names.
Unfortunately, the compiled server doesn't retain any information about the names of struct fields, so the fields still have to be reverse-engineered manually.

### Can I use this to generate stuff for other projects?
In theory, yes. Since this tool essentially just requires a list of known packet names, their IDs, and some version info, it should be easily possible to alter the scripts to generate similar code for another project.
