from rest_framework import mixins, viewsets


class CDLViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 mixins.ListModelMixin, viewsets.GenericViewSet):
    """Базовый viewset class.
    Поддерживаемые методы: Create, Destroy, List.
    """
    pass


class CRUDViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, viewsets.GenericViewSet):
    """Базовый viewset class.
    Поддерживаемые методы: Create, Destroy, List, Retrieve
    """
    pass
