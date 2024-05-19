import sys
import struct
import ctypes

class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("SizeOfStruct", ctypes.c_ulong),
        ("BaseOfCode", ctypes.c_void_p),
        ("BaseOfData", ctypes.c_void_p),
        ("ImageBase", ctypes.c_void_p),
        ("SectionAlignment", ctypes.c_ulong),
        ("FileAlignment", ctypes.c_ulong),
        ("SizeOfImage", ctypes.c_ulong),
        ("SizeOfHeaders", ctypes.c_ulong),
        ("CheckSum", ctypes.c_ulong),
        ("Subsystem", ctypes.c_ulong),
        ("DllCharacteristics", ctypes.c_ulong),
        ("SizeOfStackReserve", ctypes.c_ulong),
        ("SizeOfStackCommit", ctypes.c_ulong),
        ("SizeOfHeapReserve", ctypes.c_ulong),
        ("SizeOfHeapCommit", ctypes.c_ulong),
        ("LoaderFlags", ctypes.c_ulong),
        ("NumberOfRvaAndSizes", ctypes.c_ulong),
        ("DataDirectory", ctypes.c_ulong * 16),
    ]

def get_module_base_address(process_handle, module_name):
    module_handles = (ctypes.c_void_p * 1024)()
    module_count = ctypes.c_ulong()
    result = ctypes.windll.psapi.EnumProcessModulesEx(ctypes.c_void_p(process_handle), module_handles, ctypes.sizeof(module_handles), ctypes.byref(module_count), 0x03)
    if not result:
        raise Exception(f"Failed to enumerate modules for process {process_handle}.")

    module_base_address = None
    for i in range(module_count.value):
        module_handle = module_handles[i]
        size_ptr = ctypes.c_ulong(0)
        result = ctypes.windll.psapi.GetModuleBaseNameW(ctypes.c_void_p(process_handle), module_handle, None, ctypes.byref(size_ptr), ctypes.c_int(0))
        if not result:
            continue

        module_name_ptr = ctypes.create_string_buffer(size_ptr.value)
        result = ctypes.windll.psapi.GetModuleBaseNameW(ctypes.c_void_p(process_handle), module_handle, module_name_ptr, ctypes.byref(size_ptr), ctypes.c_int(1))
        if not result:
            continue

        module_name_str = module_name_ptr.value.decode("utf-16le")
        if module_name_str == module_name:
            module_base_address = module_handle
            break

    if module_base_address is None:
        raise Exception(f"Module '{module_name}' not found.")

    return module_base_address

def execute_lua_script(process_handle, lua_script):
    dll_name = "rbxgameapp"
    module_base_address = get_module_base_address(process_handle, dll_name)
    if not module_base_address:
        raise Exception(f"Module '{dll_name}' not found.")

    export_name ="LuaExecute"
    export_address = find_pattern(process_handle, module_base_address, f"{export_name}:")
    if not export_address:
        raise Exception(f"Export '{export_name}' not found in '{dll_name}'.")

    lua_script_ptr = ctypes.create_string_buffer(lua_script.encode("utf-8"))
    ctypes.windll.kernel32.WriteProcessMemory(ctypes.c_void_p(process_handle), ctypes.c_void_p(export_address), lua_script_ptr, len(lua_script), None)

    ctypes.windll.kernel32.CreateRemoteThread(ctypes.c_void_p(process_handle), None, 0, export_address, None, 0, None)

def find_pattern(process_handle, module_base_address, pattern):
    module_info = MODULEINFO()
    ctypes.windll.psapi.GetModuleInformation(ctypes.c_void_p(process_handle), module_base_address, ctypes.byref(module_info), ctypes.sizeof(module_info))

    start_address = module_base_address
    end_address = module_base_address + module_info.SizeOfImage

    for i in range(0, module_info.SizeOfImage - len(pattern), 1):
        current_address = start_address + i
        data = ctypes.windll.kernel32.ReadProcessMemory(ctypes.c_void_p(process_handle), ctypes.c_void_p(current_address), ctypes.c_char * len(pattern), None)
        if data.raw == pattern.encode("utf-8"):
            return current_address

    raise Exception(f"Pattern '{pattern}' not found.")

def main():
    if len(sys.argv)!= 2:
        print(f"Usage: {sys.argv[0]} <process_id>")
        return

    process_id = int(sys.argv[1])

    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if not process_handle:
        raise Exception(f"Failed to open process {process_id}.")

    lua_script = "print('Hello, World!')"
    execute_lua_script(process_handle, lua_script)

    ctypes.windll.kernel32.CloseHandle(process_handle)

if __name__ == "__main__":
    main()