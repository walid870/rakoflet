import os
import tkinter as tk
from tkinter import filedialog, messagebox

# إنشاء نافذة التطبيق الرئيسية
root = tk.Tk()
root.title("إدارة البرامج")
root.configure(bg="black")

# إزالة الشريط العلوي
root.overrideredirect(1)

# جعل التطبيق بملء الشاشة
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# قائمة لتخزين البرامج
programs = {}

# تحميل البرامج من ملف (إن وجد)
def load_programs():
    global programs
    try:
        with open("programs.txt", "r") as file:
            for line in file:
                name, path = line.strip().split("||")
                programs[name] = path
    except FileNotFoundError:
        pass

# حفظ البرامج إلى ملف
def save_programs():
    with open("programs.txt", "w") as file:
        for name, path in programs.items():
            file.write(f"{name}||{path}\n")

# التحقق من كلمة المرور
def check_password(callback):
    def validate():
        if password_entry.get() == "walid1993":  # كلمة المرور المطلوبة
            dialog.destroy()
            callback()  # استدعاء الإجراء المطلوب
        else:
            messagebox.showerror("خطأ", "كلمة المرور غير صحيحة.")

    dialog = tk.Toplevel(root)
    dialog.title("التحقق من كلمة المرور")
    dialog.geometry("300x150")
    dialog.configure(bg="black")
    tk.Label(dialog, text="أدخل كلمة المرور:", font=("Arial", 12, "bold"), fg="gold", bg="black").pack(pady=10)
    password_entry = tk.Entry(dialog, show="*", font=("Arial", 12))
    password_entry.pack(pady=10)
    tk.Button(dialog, text="تأكيد", command=validate, font=("Arial", 12), bg="gold", fg="black").pack(pady=10)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

# إضافة برنامج إلى القائمة
def add_program():
    name = name_entry.get()
    path = path_entry.get()

    if not name or not path:
        messagebox.showerror("خطأ", "الرجاء إدخال اسم البرنامج ومساره.")
        return

    if name in programs:
        messagebox.showerror("خطأ", "اسم البرنامج موجود بالفعل.")
        return

    programs[name] = path
    listbox.insert(tk.END, name)
    name_entry.delete(0, tk.END)
    path_entry.delete(0, tk.END)
    save_programs()

# اختيار مسار البرنامج عبر متصفح الملفات
def browse_program():
    def open_file_dialog():
        file_path = filedialog.askopenfilename()
        if file_path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file_path)

    # طلب كلمة المرور قبل الاستعراض
    check_password(open_file_dialog)

# تشغيل البرنامج
def run_program():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("خطأ", "الرجاء تحديد برنامج لتشغيله.")
        return

    name = listbox.get(selected[0])
    path = programs.get(name)
    if os.path.exists(path):
        os.startfile(path)
    else:
        messagebox.showerror("خطأ", "مسار البرنامج غير موجود.")

# الخروج من التطبيق
def exit_application():
    def check_password_exit():
        if password_entry.get() == "walid1993":
            root.destroy()
        else:
            messagebox.showerror("خطأ", "الرمز غير صحيح.")

    dialog = tk.Toplevel(root)
    dialog.title("إغلاق التطبيق")
    dialog.geometry("300x150")
    dialog.configure(bg="black")
    tk.Label(dialog, text="أدخل الرمز لإغلاق التطبيق:", font=("Arial", 12, "bold"), fg="gold", bg="black").pack(pady=10)
    password_entry = tk.Entry(dialog, show="*", font=("Arial", 12))
    password_entry.pack(pady=10)
    tk.Button(dialog, text="تأكيد", command=check_password_exit, font=("Arial", 12), bg="gold", fg="black").pack(pady=10)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

# تخصيص الألوان والخطوط
frame = tk.Frame(root, bg="black")
frame.pack(pady=10)

tk.Label(frame, text="اسم البرنامج:", font=("Arial", 12, "bold"), fg="gold", bg="black").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame, width=30, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="مسار البرنامج:", font=("Arial", 12, "bold"), fg="gold", bg="black").grid(row=1, column=0, padx=5, pady=5)
path_entry = tk.Entry(frame, width=30, font=("Arial", 12))
path_entry.grid(row=1, column=1, padx=5, pady=5)

browse_button = tk.Button(frame, text="استعراض", command=browse_program, font=("Arial", 12), bg="gold", fg="black")
browse_button.grid(row=1, column=2, padx=5, pady=5)

add_button = tk.Button(frame, text="إضافة", command=add_program, font=("Arial", 12), bg="gold", fg="black")
add_button.grid(row=2, column=1, pady=10)

listbox = tk.Listbox(root, width=50, height=15, font=("Arial", 12), bg="black", fg="gold")
listbox.pack(pady=10)

run_button = tk.Button(root, text="تشغيل", command=run_program, font=("Arial", 12), bg="gold", fg="black")
run_button.pack(pady=5)

# زر الخروج
exit_button = tk.Button(root, text="خروج", command=exit_application, font=("Arial", 12, "bold"), bg="red", fg="white")
exit_button.pack(side=tk.BOTTOM, pady=10)

# تحميل البرامج المحفوظة عند بدء التشغيل
load_programs()
for name in programs:
    listbox.insert(tk.END, name)

# تشغيل التطبيق
root.mainloop()
