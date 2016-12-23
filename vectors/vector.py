from math import sqrt, sin, acos, pi, degrees, floor, ceil
from decimal import Decimal, getcontext

getcontext().prec = 7

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector.'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Requires 2 or 3 coordinates.'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(Decimal(x) for x in coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty.')

        except TypeError:
            raise TypeError('The coordinates must be iterable.')

    def __str__(self):
        return 'Vector: {}'.format(str(self.coordinates))

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __getitem__(self, i):
        return self.coordinates[i]

    def __iter__(self):
        return self.coordinates.__iter__()

    def plus(self, v):
        return Vector([x + y for x,y in zip(self.coordinates, v.coordinates)])

    def minus(self, v):
        return Vector([x - y for x,y in zip(self.coordinates, v.coordinates)])
    
    def times_scalar(self, mult):
        return Vector([mult * x for x in self.coordinates])

    def magnitude(self):
        return Decimal(sqrt(sum([x**2 for x in self.coordinates])))
    
    def normalize(self):
        try:
            return self.times_scalar(Decimal('1.0')/ self.magnitude())

        except ZeroDivisionError:
            raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot_product(self, v):
        return sum([x * y for x,y in zip(self.coordinates, v.coordinates)])

    def angle(self, v, in_degrees=False):
        try: 
            in_radians = acos(self.normalize().dot_product(v.normalize()))

            if in_degrees:
                return degrees(in_radians)
            else:
                return in_radians
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector.')

    def is_parallel(self, v):
        return ( self.is_zero() or v.is_zero() or self.angle(v) == 0 or self.angle(v) == pi )

    def is_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel(self, v):
        u = v.normalize()
        return u.times_scalar(self.dot_product(u))

    def component_orthogonal(self, v):
        projection = self.component_parallel(v)
        return self.minus(projection)

    def cross_product(self, v):

        try: 
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            x_3 = y_1 * z_2 - y_2 * z_1
            y_3 = -1 * (x_1 * z_2 - x_2 * z_1)
            z_3 = x_1 * y_2 - x_2 * y_1
            return Vector([x_3, y_3, z_3])
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embdded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embdded_in_R3.cross_product(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e


    def area_of_parellelogram(self, v):
        return self.cross_product(v).magnitude()

    def area_of_triangle(self, v):
        return Decimal(0.5) * self.area_of_parellelogram(v)

''' SECTION 6 TEST
a = Vector([8.462, 7.893, -8.187])
b = Vector([6.984, -5.975, 4.778])
print 'Cross product: {}'.format(a.cross_product(b))

c = Vector([-8.987, -9.838, 5.031])
d = Vector([-4.268, -1.861, -8.866])
print 'Area of parellelogram: {}'.format(c.area_of_parellelogram(d))

e = Vector([1.5, 9.547, 3.691])
f = Vector([-6.007, 0.124, 5.772])
print 'Area of triangle: {}'.format(e.area_of_triangle(f))
'''

''' SECTION 5 TEST
a = Vector([3.039, 1.879])
b = Vector([0.825, 2.036])
print 'Projection: {}'.format(a.component_parallel(b))

c = Vector([-9.88, -3.264, -8.159])
d = Vector([-2.155, -9.353, -9.473])
print 'Component orthogonal: {}'.format(c.component_orthogonal(d))

e = Vector([3.009, -6.172, 3.692, -2.51])
f = Vector([6.404, -9.144, 2.759, 8.718])
print 'Projection: {}'.format(e.component_parallel(f))
print 'Component orthogonal: {}'.format(e.component_orthogonal(f))
'''

''' SECTION 4 TEST
a = Vector([-7.579, -7.88])
b = Vector([22.737, 23.64])
print a.is_parallel(b) (Returns False. Should be True. Accuracy issue?)
print a.is_orthogonal(b)

c = Vector([-2.029, 9.97, 4.172])
d = Vector([-9.231, -6.639, -7.245])
print c.is_parallel(d)
print c.is_orthogonal(d)

e = Vector([-2.328, -7.284, -1.214])
f = Vector([-1.821, 1.072, -2.94])
print e.is_parallel(f)
print e.is_orthogonal(f)

g = Vector([2.118, 4.827])
h = Vector([0, 0])
print g.is_parallel(h)
print g.is_orthogonal(h)
'''

''' SECTION 3 TEST
a = Vector([7.887, 4.138])
b = Vector([-8.802, 6.776])
print 'Dot product: {}'.format(a.dot_product(b))

c = Vector([-5.955, -4.904, -1.874])
d = Vector([-4.496, -8.755, 7.103])
print 'Dot product: {}'.format(c.dot_product(d))

e = Vector([3.183, -7.627])
f = Vector([-2.668, 5.319])
print 'Angle: {}'.format(e.angle(f))

g = Vector([7.35, 0.221, 5.188])
h = Vector([2.751, 8.259, 3.985])
print 'Angle: {}'.format(g.angle(h, True))
'''

''' SECTION 2 TEST
a = Vector([-0.221, 7.437])
print 'Magnitude: {}'.format(a.magnitude())
b = Vector([8.813, -1.331, -6.247])
print 'Magnitude: {}'.format(b.magnitude())
c = Vector([5.581, -2.136])
print 'Direction: {}'.format(c.normalize())
d = Vector([1.996, 3.108, -4.554])
print 'Direction: {}'.format(d.normalize())
'''

''' SECION 1 TEST
a = Vector([8.218, -9.341])
b = Vector([-1.129, 2.111])
print 'Plus: {}'.format(a.plus(b))

c = Vector([7.119, 8.215])
d = Vector([-8.223, 0.878])
print 'Minus: {}'.format(c.minus(d))

e = Vector([1.671, -1.012, -0.318])
print 'Multiply: {}'.format(e.times_scalar(Decimal(7.41)))
'''
