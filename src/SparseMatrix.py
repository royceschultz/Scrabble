class SparseMatrix(dict):
    def __init__(self, d={}):
        super()
        self.update(d)

    def get_axis(self, axis):
        return [i[axis] for i in self.keys()]

    def toString(self, default='.', fill={}, overlay={}):
        rep = ''
        xs = self.get_axis(0) + [0]
        ys = self.get_axis(1) + [0]
        x_range = max(xs) - min(xs)
        y_range = max(ys) - min(ys)
        if max(x_range, y_range) < 20:
            for i in range(min(xs), max(xs) + 1):
                for j in range(min(ys), max(ys) + 1):
                    p = (i,j)
                    if p in overlay:
                        rep += f' {str(overlay[p]):3s} '
                    elif p in self:
                        rep += f' {str(self[p]):3s} '
                    elif p in fill:
                        rep += f'*{str(fill[p]):3s}*'
                    else:
                        rep += f' {str(default):3s} '
                rep += '\n'
        return rep
