# UT0203 - Use encrypted devices

**Tactic:** [UTA02 - Technical Safeguarding](./README.md)

## Description

The handler may implement encryption across all operational devices to mitigate the risks associated with data exposure in the event of loss or theft. This technique is critical not only for maintaining the confidentiality of the data but also for preserving the integrity and availability of information crucial to the operation.

Linux devices. Implement encryption using LUKS (Linux Unified Key Setup), which is integrated with the system's volume management. This method offers strong encryption that secures the entire disk, including swap spaces and temporary files, ensuring that all aspects of the device are protected.

MacOS devices. Implement encryption using FileVault to provide full-disk encryption, which automatically encrypts the entire system drive and any files added to it, securing the device with powerful user authentication during startup.

Windows devices, BitLocker is the standard encryption tool provided by Microsoft. It offers full-disk encryption, which encrypts the entire drive where Windows and user data reside. BitLocker integrates with the Trusted Platform Module (TPM) hardware on the device to ensure that the encryption keys are stored securely and are only accessible upon successful authentication.

iOS devices. iOS uses built-in encryption that is automatically enabled when a user sets a passcode.

Android devices. Adopt full-disk encryption using AES (Advanced Encryption Standard) or file-based encryption, depending on the version of the operating system. Newer versions of Android support file-based encryption which allows encrypted files to be individually locked or unlocked, providing more granular access controls alongside traditional full-disk encryption methods.

Other operating systems and devices may be added depending on the operational needs. In any case, participants should be trained and guided to use them safely.
