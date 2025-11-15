# Unused Commands in luminous.py

## Phân tích các class/function không được sử dụng

### ✅ ĐƯỢC SỬ DỤNG (giữ lại):
1. **Attack** - Dùng trong test routines
2. **Reflection** - Dùng trong routine
3. **Reflection_Random** - Dùng trong routine
4. **Reflection_Mix_Random** - Dùng phổ biến trong routine
5. **Teleport** - Dùng trong routine
6. **Teleport_Up** - Dùng trong routine
7. **Teleport_Down** - Dùng trong routine
8. **Jump_Teleport_Up** - Dùng trong routine
9. **Jump_Down** - Dùng trong routine
10. **Buff** - Dùng trong routine
11. **Buff_Secondary** - Dùng trong routine
12. **Face_Right** - Dùng trong routine
13. **Face_Left** - Dùng trong routine
14. **Adjust** - Được gọi tự động bởi Move class khi `adjust=True`
15. **step()** function - Được gọi từ Move class trong `src/routine/components.py`
16. **Random_Teleport** - Dùng trong test routine
17. **Random_Attack** - Dùng trong test routine
18. **Random_Skill** - Dùng trong test routine
19. **Conditional_Action** - Dùng trong test routine

### ❌ KHÔNG ĐƯỢC SỬ DỤNG (có thể xóa):

#### 1. **Apocalypse** (class, lines 182-188)
- **Lý do**: Không thấy trong routine files
- **Lưu ý**: Được dùng trong `Reflection_Mix_Random` và `Apocalypse_Or_Scythe`, nhưng class riêng không được gọi trực tiếp

#### 2. **Death_Scythe** (class, lines 190-201)
- **Lý do**: Không thấy trong routine files
- **Lưu ý**: Được dùng trong `Reflection_Mix_Random` và `Apocalypse_Or_Scythe`, nhưng class riêng không được gọi trực tiếp

#### 3. **Apocalypse_Or_Scythe** (class, lines 203-226)
- **Lý do**: Không thấy trong routine files
- **Lưu ý**: Có thể hữu ích cho tương lai nhưng hiện tại không dùng

#### 4. **Light_Reflection** (class, lines 228-234)
- **Lý do**: Không thấy trong routine files
- **Lưu ý**: Được dùng trong `Random_Skill` test routine, nhưng class riêng không được gọi trực tiếp

#### 5. **Dark_Reflection** (class, lines 236-242)
- **Lý do**: Không thấy trong routine files
- **Lưu ý**: Không được dùng ở đâu cả

#### 6. **Jump** (class, lines 387-401)
- **Lý do**: Không thấy trong routine files
- **Lưu ý**: Có `Jump_Teleport_Up` và `Jump_Down` được dùng, nhưng `Jump` đơn giản không được dùng

## Khuyến nghị:

### Có thể xóa an toàn:
- **Dark_Reflection** - Hoàn toàn không được dùng
- **Jump** - Có các variant khác được dùng thay thế

### Nên giữ lại (có thể dùng trong tương lai):
- **Apocalypse** - Có thể dùng riêng lẻ
- **Death_Scythe** - Có thể dùng riêng lẻ
- **Apocalypse_Or_Scythe** - Có thể hữu ích cho routine tùy chỉnh
- **Light_Reflection** - Có thể dùng riêng lẻ

## Lưu ý:
- Các class được dùng trong `Reflection_Mix_Random` (như `Apocalypse`, `Death_Scythe`) vẫn cần thiết vì chúng được gọi gián tiếp
- `step()` function được gọi từ Move class, không phải từ routine CSV, nên phải giữ lại

