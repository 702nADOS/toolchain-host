#pragma once

#include <session/session.h>
#include <base/rpc.h>
#include <ram_session/ram_session.h>
#include <string>

struct Task_manager_session : Genode::Session
{
	static const char *service_name() { return "task-manager"; }

	virtual void add_tasks(Genode::Ram_dataspace_capability xml_ds_cap) = 0;
	virtual void clear_tasks() = 0;
	virtual Genode::Ram_dataspace_capability binary_ds(Genode::Ram_dataspace_capability name_ds_cap, size_t size) = 0;
	virtual void start() = 0;
	virtual void stop() = 0;
	virtual Genode::Ram_dataspace_capability profile_data() = 0;

	/*******************
	 ** RPC interface **
	 *******************/
	GENODE_RPC(Rpc_add_tasks, void, add_tasks, Genode::Ram_dataspace_capability);
	GENODE_RPC(Rpc_clear_tasks, void, clear_tasks);
	GENODE_RPC(Rpc_binary_ds, Genode::Ram_dataspace_capability, binary_ds, Genode::Ram_dataspace_capability, size_t);
	GENODE_RPC(Rpc_start, void, start);
	GENODE_RPC(Rpc_stop, void, stop);
	GENODE_RPC(Rpc_profile_data, Genode::Ram_dataspace_capability, profile_data);

	GENODE_RPC_INTERFACE(Rpc_add_tasks, Rpc_clear_tasks, Rpc_binary_ds, Rpc_start, Rpc_stop, Rpc_profile_data);
};
