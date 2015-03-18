r"""
Examples of a finite dimensional Lie algebra with basis
"""
#*****************************************************************************
#  Copyright (C) 2014 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.sets.family import Family
from sage.categories.all import LieAlgebras
from sage.rings.all import ZZ
from sage.modules.free_module import FreeModule
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.categories.examples.lie_algebras import LieAlgebraFromAssociative as BaseExample

class AbelianLieAlgebra(Parent, UniqueRepresentation):
    r"""
    An example of a finite dimensional Lie algebra with basis:
    the abelian Lie algebra.

    Let `R` be a commutative ring, and `M` an `R`-module. The
    *abelian Lie algebra* on `M` is the `R`-Lie algebra
    obtained by endowing `M` with the trivial Lie bracket
    (`[a, b] = 0` for all `a, b \in M`).

    This class illustrates a minimal implementation of a finite dimensional
    Lie algebra with basis.

    INPUT:

    - ``R`` -- base ring

    - ``n`` -- (optional) a nonnegative integer (default: ``None``)

    - ``M`` -- an `R`-module (default: the free `R`-module of
      rank ``n``) to serve as the ground space for the Lie algebra

    - ``ambient`` -- (optional) a Lie algebra; if this is set,
      then the resulting Lie algebra is declared a Lie subalgebra
      of ``ambient``

    OUTPUT:

    The abelian Lie algebra on `M`.
    """
    @staticmethod
    def __classcall_private__(cls, R, n=None, M=None, ambient=None):
        """
        Normalize input to ensure a unique representation.

        EXAMPLES::

            sage: from sage.categories.examples.finite_dimensional_lie_algebras_with_basis import AbelianLieAlgebra
            sage: A1 = AbelianLieAlgebra(QQ, n=3)
            sage: A2 = AbelianLieAlgebra(QQ, M=FreeModule(QQ, 3))
            sage: A3 = AbelianLieAlgebra(QQ, 3, FreeModule(QQ, 3))
            sage: A1 is A2 and A2 is A3
            True

            sage: A1 = AbelianLieAlgebra(QQ, 2)
            sage: A2 = AbelianLieAlgebra(ZZ, 2)
            sage: A1 is A2
            False

            sage: A1 = AbelianLieAlgebra(QQ, 0)
            sage: A2 = AbelianLieAlgebra(QQ, 1)
            sage: A1 is A2
            False
        """
        if M is None:
            M = FreeModule(R, n)
        else:
            M = M.change_ring(R)
        return super(AbelianLieAlgebra, cls).__classcall__(cls, R, n=None, M=M, ambient=ambient)

    def __init__(self, R, n=None, M=None, ambient=None):
        """
        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: TestSuite(L).run()
        """
        self._M = M
        cat = LieAlgebras(R).FiniteDimensional().WithBasis()
        if ambient is None:
            ambient = self
        else:
            cat = cat.Subobjects()
        self._ambient = ambient
        Parent.__init__(self, base=R, category=cat)

    def _repr_(self):
        """
        EXAMPLES::

            sage: LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            An example of a finite dimensional Lie algebra with basis:
             the 3-dimensional abelian Lie algebra over Rational Field
        """
        ret = "An example of a finite dimensional Lie algebra with basis:" \
              " the {}-dimensional abelian Lie algebra over {}".format(
                         self.n(), self.base_ring())
        B = self._M.basis_matrix()
        if not B.is_one():
            ret += " with basis matrix:\n{!r}".format(B)
        return ret

    def n(self):
        return self._M.rank()

    def _element_constructor_(self, x):
        """
        Construct an element of ``self`` from ``x``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L(0)
            (0, 0, 0)
            sage: M = FreeModule(ZZ, 3)
            sage: L(M([1, -2, 2]))
            (1, -2, 2)
            sage: a,b,c = L.lie_algebra_generators()
            sage: X = L.subalgebra([a+b, 2*a+c])
            sage: x,y = X.basis()
            sage: L(x)
            (1, 0, 1/2)
            sage: L(x+y)
            (1, 1, 0)
        """
        if isinstance(x, AbelianLieAlgebra.Element):
            x = x.value
        return self.element_class(self, self._M(x))

    @cached_method
    def zero(self):
        """
        Return the zero element.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.zero()
            (0, 0, 0)
        """
        return self.element_class(self, self._M.zero())

    def basis_matrix(self):
        """
        Return the basis matrix of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.basis_matrix()
            [1 0 0]
            [0 1 0]
            [0 0 1]
        """
        return self._M.basis_matrix()

    def ambient(self):
        """
        Return the ambient Lie algebra of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: a, b, c = L.lie_algebra_generators()
            sage: S = L.subalgebra([2*a+b, b + c])
            sage: S.ambient() == L
            True
        """
        return self._ambient

    def subalgebra(self, gens):
        """
        Return the Lie subalgebra of ``self`` generated by the
        elements of the iterable ``gens``.

        This currently requires the ground ring `R` to be a field.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: a, b, c = L.lie_algebra_generators()
            sage: L.subalgebra([2*a+b, b + c])
            An example of a finite dimensional Lie algebra with basis:
             the 2-dimensional abelian Lie algebra over Rational Field with
             basis matrix:
            [   1    0 -1/2]
            [   0    1    1]
        """
        N = self._M.subspace([g.value for g in gens])
        return AbelianLieAlgebra(self.base_ring(), M=N, ambient=self._ambient)

    def basis(self):
        """
        Return the basis of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.basis()
            Finite family {0: (1, 0, 0), 1: (0, 1, 0), 2: (0, 0, 1)}
        """
        d = {i: self.element_class(self, b)
             for i,b in enumerate(self._M.basis())}
        return Family(d)

    lie_algebra_generators = basis

    def gens(self):
        """
        Return the generators of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.gens()
            ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        """
        return tuple(self._M.basis())

    def free_module(self):
        """
        Return ``self`` as a free module.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.free_module()
            Vector space of dimension 3 over Rational Field

            sage: a, b, c = L.lie_algebra_generators()
            sage: S = L.subalgebra([2*a+b, b + c])
            sage: S.free_module()
            Vector space of degree 3 and dimension 2 over Rational Field
            Basis matrix:
            [   1    0 -1/2]
            [   0    1    1]
        """
        return self._M

    class Element(BaseExample.Element):
        def __iter__(self):
            """
            Iterate over ``self`` by returning pairs ``(i, c)`` where ``i``
            is the index of the basis element and ``c`` is the corresponding
            coefficient.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: a, b, c = L.lie_algebra_generators()
                sage: elt = 2*a - c
                sage: list(elt)
                [(0, 2), (2, -1)]
            """
            zero = self.parent().base_ring().zero()
            for i, c in self.value.iteritems():
                if c != zero:
                    yield (i, c)

        def __getitem__(self, i):
            """
            Redirect the ``__getitem__()`` to the wrapped element unless
            ``i`` is a basis index.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: a, b, c = L.lie_algebra_generators()
                sage: elt = 2*a + b - c
                sage: elt[0]
                2
                sage: elt[2]
                -1
            """
            return self.value.__getitem__(i)

        def _bracket_(self, y):
            """
            Return the Lie bracket ``[self, y]``.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: a, b, c = L.lie_algebra_generators()
                sage: a.bracket(c)
                (0, 0, 0)
                sage: a.bracket(b).bracket(c)
                (0, 0, 0)
            """
            return self.parent().zero()

        def lift(self):
            """
            Return the lift of ``self`` to the universal enveloping algebra.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: a, b, c = L.lie_algebra_generators()
                sage: elt = 2*a + 2*b + 3*c
                sage: elt.lift()
                2*a + 2*b + 3*c
            """
            UEA = self.parent().universal_enveloping_algebra()
            gens = UEA.gens()
            return UEA.sum(c * gens[i] for i, c in self.value.iteritems())

        def to_vector(self):
            """
            Return ``self`` as a vector.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: a, b, c = L.lie_algebra_generators()
                sage: elt = 2*a + 2*b + 3*c
                sage: elt.to_vector()
                (2, 2, 3)
            """
            return self.value

Example = AbelianLieAlgebra

