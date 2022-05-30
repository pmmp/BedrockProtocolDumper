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

/**
 * Version numbers and packet IDs for the current Minecraft PE protocol
 */
final class ProtocolInfo{

	private function __construct(){
		//NOOP
	}

	/**
	 * NOTE TO DEVELOPERS
	 * Do not waste your time or ours submitting pull requests changing game and/or protocol version numbers.
	 * Pull requests changing game and/or protocol version numbers will be closed.
	 *
	 * This file is generated automatically, do not edit it manually.
	 */

	/** Actual Minecraft: PE protocol version */
	public const CURRENT_PROTOCOL = %d;
	/** Current Minecraft PE version reported by the server. This is usually the earliest currently supported version. */
	public const MINECRAFT_VERSION = '%s';
	/** Version number sent to clients in ping responses. */
	public const MINECRAFT_VERSION_NETWORK = '%s';

%s
}
