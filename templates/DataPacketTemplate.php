<?php

/*
 * This file is part of BedrockProtocol.
 * Copyright (C) 2014-2022 PocketMine Team <https://github.com/pmmp/BedrockProtocol>
 *
 * BedrockProtocol is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

declare(strict_types=1);

namespace pocketmine\network\mcpe\protocol;

use pocketmine\network\mcpe\protocol\serializer\PacketSerializer;

class %s extends DataPacket{
	public const NETWORK_ID = ProtocolInfo::%s;

	/**
	 * @generate-create-func
	 */
	public static function create() : self{
		$result = new self;
		//TODO: add fields
		return $result;
	}

	protected function decodePayload(PacketSerializer $in) : void{
		//TODO
	}

	protected function encodePayload(PacketSerializer $out) : void{
		//TODO
	}

	public function handle(PacketHandlerInterface $handler) : bool{
		return $handler->handle%s($this);
	}
}
