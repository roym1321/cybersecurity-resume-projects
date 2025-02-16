// Inject DLL to a running process - THE DLL NEEDS TO BE 32 BIT, CURRENTLY DOESNT WORK
#include <stdio.h>
#include <windows.h>
#define NOTPAD_PID 4040
#define DLL_PATH "C:\\Users\\Roy\\source\\repos\\mydll\\x64\\Release\\mydll.dll"

DWORD getdllFullPath(PCHAR dll_FileName, PCHAR dll_Path)
{
    // Get the full path of the DLL on dll_FileName.
    // Return its length or abort program.
    DWORD pathLen = GetFullPathNameA(dll_FileName, MAX_PATH, dll_Path, NULL);
    if (pathLen > 0) 
    {
        printf("The full path of %s is: %s\n", dll_FileName, dll_Path);
    } 
    else 
    {
        printf("GetFullPathName failed with error code: %d\n", GetLastError());
        abort();
    }
    return pathLen;
}

HANDLE getProcessHandle(DWORD pid)
{
    // Open remote process using its ID.
    // Return its handle or abort program.
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess != NULL) 
    {
        printf("OpenProcess succeeded\n");
    } 
    else 
    {
        printf("OpenProcess failed, Error code: %d\n", GetLastError());
        abort();
    }
    return hProcess;
}

PVOID getProcessMemoryAddress(HANDLE hProcess, DWORD buffSize)
{
    // Allocate Memory with the size of DLL name inside the remote process.
    // Return its pointer or abort the program.
    PVOID memAddr = (PVOID)VirtualAllocEx(hProcess,
                                            NULL,
                                            buffSize,
                                            MEM_COMMIT | MEM_RESERVE,
                                            PAGE_EXECUTE_READWRITE);
    if (NULL != memAddr) 
    {
        printf("Received Process Memory Address\n");
    }
    else if (GetLastError()== ERROR_ACCESS_DENIED)
    {
        printf("Failed to receive Process Memory Address: ERROR_ACCESS_DENIED\n");
    }
    else
    {
        printf("Failed to receive Process Memory Address: %d\n", GetLastError());
        abort();
    }
    return memAddr;
}

PVOID writeDLLNameToProcessMemory(HANDLE hProcess, DWORD dllPathLen, PCHAR dllPath)
{
    // Write DLL name to remote allocated process memory.
    //If failed abort the program.
    PVOID pRemoteDLLName = getProcessMemoryAddress(hProcess, dllPathLen);

    SIZE_T lpNumberOfBytesWritten;
    BOOL check = WriteProcessMemory(hProcess, pRemoteDLLName, dllPath, dllPathLen, &lpNumberOfBytesWritten);
    if (0 == check) {
        printf("Failed to Write Memory: %d\n", GetLastError());
        abort();
    }
    else
    {
        printf("The DLL path (%d) was successfuly written to the Process Memory.\n",
         lpNumberOfBytesWritten);
    }
    return pRemoteDLLName;
}

HANDLE runDLLRemoteThread(HANDLE hProcess, PVOID pRemoteDLLName)
{
    // Get LoadLibrary function address –
    // the address doesn't change at remote process
    LPVOID pLoadLibraryA = (PVOID)GetProcAddress(GetModuleHandle("kernel32.dll"),
                            "LoadLibraryA");
    DWORD lpThreadId;
    HANDLE hRemoteThread = CreateRemoteThread(hProcess,
     NULL, 0, pLoadLibraryA, pRemoteDLLName, 0, &lpThreadId);
    
    if (NULL == hRemoteThread) {
        printf("Failed to Create Thread: %d\n", GetLastError());
        abort();
    }
    else
    {
        printf("Created Thread successfuly with the ID: %d.\n", lpThreadId);
        return hRemoteThread;
    }
}

int main()
{
    HANDLE current = GetCurrentProcess();

    CHAR dllPath[MAX_PATH] = DLL_PATH;
    CHAR dllFileName[] = "mydll.dll";
    DWORD dwPid = NOTPAD_PID;
    //DWORD dllPathLen = getdllFullPath(dllFileName, dllPath);
    DWORD dllPathLen = strlen(dllPath);
    HANDLE hProcess = getProcessHandle(dwPid);

    PVOID pRemoteDLLName = writeDLLNameToProcessMemory(hProcess, dllPathLen, dllPath);

    HANDLE hRemoteThread = runDLLRemoteThread(hProcess, pRemoteDLLName);

    WaitForSingleObject(hRemoteThread, INFINITE);
    CloseHandle(hRemoteThread);
    CloseHandle(hProcess);
    return 0;
}

