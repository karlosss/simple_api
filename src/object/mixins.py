class ListMixin:
    def list(self, *args, **kwargs):
        raise NotImplementedError


class DetailMixin:
    def detail(self, id, *args, **kwargs):
        raise NotImplementedError


class CreateMixin:
    def create(self, *args, **kwargs):
        raise NotImplementedError


class UpdateMixin:
    def update(self, *args, **kwargs):
        raise NotImplementedError


class DeleteMixin:
    def delete(self, *args, **kwargs):
        raise NotImplementedError
