<?php

/*
 *
 *  ____            _        _   __  __ _                  __  __ ____
 * |  _ \ ___   ___| | _____| |_|  \/  (_)_ __   ___      |  \/  |  _ \
 * | |_) / _ \ / __| |/ / _ \ __| |\/| | | '_ \ / _ \_____| |\/| | |_) |
 * |  __/ (_) | (__|   <  __/ |_| |  | | | | | |  __/_____| |  | |  __/
 * |_|   \___/ \___|_|\_\___|\__|_|  |_|_|_| |_|\___|     |_|  |_|_|
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * @author PocketMine Team
 * @link http://www.pocketmine.net/
 *
 *
 */

declare(strict_types=1);

namespace pocketmine\network\mcpe\protocol;

use pocketmine\utils\Binary;
use pocketmine\utils\BinaryDataException;

class PacketPool{
	/** @var self|null */
	protected static ?PacketPool $instance = null;

	public static function getInstance() : self{
		if(self::$instance === null){
			self::$instance = new self;
		}
		return self::$instance;
	}

	/** @var \SplFixedArray<Packet> */
	protected \SplFixedArray $pool;

	public function __construct(){
		$this->pool = new \SplFixedArray(%d);
%s
	}

	public function registerPacket(Packet $packet) : void{
		$this->pool[$packet->pid()] = clone $packet;
	}

	public function getPacketById(int $pid) : ?Packet{
		return isset($this->pool[$pid]) ? clone $this->pool[$pid] : null;
	}

	/**
	 * @throws BinaryDataException
	 */
	public function getPacket(string $buffer) : ?Packet{
		$offset = 0;
		return $this->getPacketById(Binary::readUnsignedVarInt($buffer, $offset) & DataPacket::PID_MASK);
	}
}
