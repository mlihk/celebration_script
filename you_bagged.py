import tkinter as tk
from tkinter import messagebox
import random

# Password
CORRECT_PASSWORD = "bagged"

class PasswordApp:
    def __init__(self, root, app_list):
        self.root = root
        self.app_list = app_list  # Reference to list of all app instances
        self.root.title("Password Prompt")
        
        # Prevent window from closing via window manager
        self.root.protocol("WM_DELETE_WINDOW", self.prevent_close)
        
        # GUI elements
        self.label = tk.Label(root, text="Enter password:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root, show="*")
        self.entry.pack(pady=5)
        
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)
        
        self.submit_button = tk.Button(root, text="Submit", command=self.check_password)
        self.submit_button.pack(pady=5)
        
        # Bind Enter key to submit
        self.root.bind('<Return>', lambda event: self.check_password())
        
    def prevent_close(self):
        # Prevent closing the window
        messagebox.showwarning("Warning", "Cannot close window until correct password is entered!")
        
    def check_password(self):
        user_input = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        
        if user_input == CORRECT_PASSWORD:
            self.status_label.config(text="Correct password! Closing all windows...")
            # Close all password windows
            for app in self.app_list:
                app.root.destroy()
            # Show celebration window
            self.show_celebration()
        else:
            self.status_label.config(text="Incorrect password!")
            # Double the number of windows
            current_count = len(self.app_list)
            for _ in range(current_count):
                new_root = tk.Tk()
                new_root.geometry("300x150")
                new_app = PasswordApp(new_root, self.app_list)
                self.app_list.append(new_app)

    def show_celebration(self):
        # Create celebration window
        celeb_root = tk.Tk()
        celeb_root.title("Congratulations!")
        celeb_root.geometry("400x300")
        
        # Bind Esc key to close the celebration window
        celeb_root.bind('<Escape>', lambda event: celeb_root.destroy())
        
        # Canvas for animation
        canvas = tk.Canvas(celeb_root, width=400, height=300, bg="black")
        canvas.pack()
        
        # Congrats message
        canvas.create_text(200, 50, text="Congrats, you bagged the job!", fill="white", 
                          font=("Arial", 16, "bold"))
        
        # Particle animation
        particles = []
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        
        def create_particle():
            x = random.randint(0, 400)
            y = 300  # Start at bottom
            size = random.randint(5, 10)
            color = random.choice(colors)
            particle = canvas.create_oval(x, y, x+size, y+size, fill=color)
            velocity = random.randint(-5, 5), random.randint(-10, -5)  # x, y velocity
            return particle, velocity
        
        # Create initial particles
        for _ in range(20):
            particle, velocity = create_particle()
            particles.append((particle, velocity))
        
        def animate_particles():
            for i, (particle, velocity) in enumerate(particles):
                vx, vy = velocity
                canvas.move(particle, vx, vy)
                # Update velocity for gravity-like effect
                vy += 0.1  # Simulate gravity
                particles[i] = (particle, (vx, vy))
                
                # Get current position
                x1, y1, x2, y2 = canvas.coords(particle)
                # Remove particle if off-screen
                if y1 > 300 or x1 < 0 or x2 > 400:
                    canvas.delete(particle)
                    new_particle, new_velocity = create_particle()
                    particles[i] = (new_particle, new_velocity)
            
            # Continue animation
            celeb_root.after(50, animate_particles)
        
        # Start animation
        animate_particles()
        
        # Close button for celebration window
        close_button = tk.Button(celeb_root, text="Close", command=celeb_root.destroy)
        close_button.pack(pady=10)
        
        celeb_root.mainloop()

def main():
    app_list = []
    root = tk.Tk()
    root.geometry("300x150")  # Set window size
    app = PasswordApp(root, app_list)
    app_list.append(app)
    root.mainloop()

if __name__ == "__main__":
    main()
