function Test-Administrator  
{  
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    return (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)  
}

function Disable-CAD{
    try{
        Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentvERSION\Policies\System" -Name disablecad -Value 1
        write-host "CAD disabled successfully"
    }
    catch{
        write-host "CAD couldn't be disabled"
    }
}

function Disable-PasswordComplexity(){
    try{
        $domain_forest = (Get-ADDomain | Select-Object -Property forest).forest
        Set-ADDefaultDomainPasswordPolicy -Identity $domain_forest -ComplexityEnabled $false -MinPasswordLength 4
        write-host "Password Policy for $domain_forest changed successfully."
        return $true
    }
    catch{
        write-host "Couldn't change the password policy for the domain (maybe does not exist)"
        return $false
    }
}


function ChangePassword(){
    while($True) {
        $new_password = Read-Host "Enter the password you want to change to"
        if ($new_password.Length -lt 4) {
            write-host 'The password has to be greater than 3 letters'
            continue
        }
        else {
            try {
                net user $username $new_password
                write-host "Password changed successfuly."
                break
            }
            catch {
                write-host "Couldn't change the password for user $username"
                break
            }
        }
    } 
}  

function Enable_Numpad(){
    try{    
        New-PSDrive HKU Registry HKEY_USERS
        set-ItemProperty -path 'HKU:\.DEFAULT\Control Panel\Keyboard' -name InitialKeyboardIndicators -Value 2147483650
        write-host "NumPad enabled successfully"
        break
    }
    catch{
        write-host "NumPad couldn't be enabled"
        break
    }
}


    $is_user_administrator = Test-Administrator
    if (!$is_user_administrator){
        write-host "Please run the script as administrator."
        exit
    }
    else {
        write-host "Hello $env:USERNAME"
    }

    while($true) {
        $answer = read-host "Do you want to disable Ctrl+Alt+Del when signing in? (Y/N)"
        if ($answer.ToUpper() -eq "Y") {
            Disable-CAD
            break
        }
        elseif ($answer.ToUpper() -eq "N"){
            break
        } 
    }

    while($true) {
        $answer = read-host "Do you want to enable NumPad when signing in? (Y/N)"
         if ($answer.ToUpper() -eq "Y") {
            Enable_Numpad
         }
         elseif ($answer.ToUpper() -eq "N"){
             break
         } 
    }

    while ($True) {
        $answer = read-host "Do you want to disable Password Complexity and reduce it's length to 4 letters? (Y/N)"
        if ($answer.ToUpper() -eq "Y") {
            Disable-PasswordComplexity
            break
        } 
        elseif ($answer.ToUpper() -eq "N"){
            pause
            exit
        } 
    }

    while ($True) {
        $answer = read-host "Do you want to Change your password? (Y/N)"
        if ($answer.ToUpper() -eq "Y") {
		Set-ADAccountPassword -Identity $env:USERNAME -NewPassword (read-Host "Type the new Password:" -AsSecureString)
		break
        }
        elseif ($answer.ToUpper() -eq "N"){
            break
        }
    }

    pause
    