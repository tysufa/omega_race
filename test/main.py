import moderngl_window as mglw


class App(mglw.WindowConfig):
    window_size = 1600, 900
    ressource_dir = 'programs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='fragment_shader.glsl')

    def render(self, time: float, frame_time: float):
        self.ctx.clear()
        self.quad.render(self.prog)

if __name__ == '__main__':
    mglw.run_window_config(App)
