IDEAL
MODEL small
STACK 100h
DATASEG
x dw 50
y dw 75
color dw 15 ;White
color2 dw 4 ; Red
tiles_x dw 50, 75, 100, 125, 150, 175, 200, 225
keys db 01Eh, 01Fh, 20h, 21h, 22h, 23h, 24h, 25h ;'asdfghjk' 
SaveKey db ?
msg db 'Press the buttons to play', 10, 13
	db 'Esc to exit', 10, 13, '$'
C_note dw 11CAh
D_note dw 0FDAh
E_note dw 0E1Fh
F_note dw 0D5Ah
G_note dw 0BE3h
A_note dw 0A97h
B_note dw 096Fh

CODESEG


proc Set_TextMode ;Change the graphics to Text Mode.
	push ax
	mov ah, 0h
	mov al, 2h
	int 10h
	pop ax
	ret
endp Set_TextMode


proc Set_GraphicMode
	push ax
	; Set graphics mode 320x200x256 (x < 320, y < 200, 256 colors)
	mov ax, 13h
	int 10h
	pop ax
	ret
endp Set_GraphicMode



tile_x equ [word bp+4]
tile_y equ [word bp+6]
tile_color equ [byte bp+8]
proc Print_Tile
	push bp
	mov bp, sp
	push ax
	push bx
	push cx
	push dx
	
	mov cx, 50 ;Length
	mov ax, tile_x
	create_tile:
		push cx
		push ax
		mov cx, 20 ;Width
		print_line:
			mov bh,0h ; Page (needs to be 0)
			push cx
			
			mov cx,tile_x ;x
			mov dx,tile_y ;y
			mov al,tile_color ; Color
			mov ah,0ch
			int 10h

			inc tile_x
			pop cx
			loop print_line
		inc tile_y ;go down one
		pop ax
		mov tile_x, ax
		pop cx
	loop create_tile
	
	pop dx
	pop cx
	pop bx
	pop ax
	pop bp
	ret 6
endp Print_Tile


proc Print_Piano
	push cx
	push bx
	
	mov cx, 8
	lea bx, [tiles_x]
	Print:
		push [color]
		push [y]
		push [bx] ; x
		call Print_Tile
		add bx, 2
		loop Print
	
	pop bx
	pop cx
	ret
endp Print_Piano

start:
	mov ax, @data
	mov ds, ax
	call Set_GraphicMode
	
	call Print_Piano
	
	print_msg:
		mov dx, offset msg
		mov ah, 9h
		int 21h
	
	
	WaitForData:
		mov ah, 1 
		int 16h ; Checks status of keybord (if there is data waiting).
		jz WaitForData ;If 0, there is no data. else, al will receive ASCII and ah scan code.
		in al, 60h
		
		cmp al, 1h
		je exit1
		
		cmp al, [SaveKey]
		je WaitForData
		mov [SaveKey], al
		
		push ax
		and al, 80h
		jnz jmp_off	
		pop ax
		
		
		mov cx, 8
		mov bx, offset keys
		correct_keys:
			cmp al, [bx]
			je key_found
			inc bx
			loop correct_keys
		
		
		jmp WaitForData
	
	exit1:
		jmp exit
	
	jmp_off:
		jmp sound_off
	
	key_found:
		
		lea bx, [tiles_x]
		
		cmp al, 01Eh ; a = C
		mov dx, [C_note]
		je sound_on
		
		add bx, 2
		cmp al, 01Fh ; s = D
		mov dx, [D_note]
		je sound_on
		
		add bx, 2
		cmp al, 20h ; d = E
		mov dx, [E_note]
		je sound_on
		
		add bx, 2
		cmp al, 21h ; f = F
		mov dx, [F_note]
		je sound_on
		
		add bx, 2
		cmp al, 22h ; g = G
		mov dx, [G_note]
		je sound_on
		
		add bx, 2
		cmp al, 23h ; h = A
		mov dx, [A_note]
		je sound_on
		
		add bx, 2
		cmp al, 24h ; j = B
		mov dx, [B_note]
		je sound_on
		
		push ax
		mov dl, al
		mov ah, 2h
		int 21h
		pop ax
		
		jmp WaitForData
		sound_on:
			push [color2]
			push [y]
			push [bx] ; x
			call Print_Tile
		
		
			in al, 61h
			or al, 00000011b
			out 61h, al
			mov al, 0b6h
			out 43h, al
			
			mov al, dl
			out 42h, al
			mov al, dh
			out 42h, al
			jmp WaitForData
			
		sound_off:
			pop ax
			
			call Print_Piano
			
			in al, 61h
			and al, 11111100b
			out 61h, al
			jmp WaitForData
		
exit:
	; Wait for key press
	mov ah, 0h
	int 16h
	call Set_TextMode
	mov ax, 4C00h
	int 21h
END start