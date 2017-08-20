from .forms import CreateCommentForm


def make_new_form(request, obj_id, c_type):
    if request.user.is_authenticated():
        initial = {
            "content_type": c_type,
            "object_id": obj_id,
        }
        form = CreateCommentForm(initial=initial)
        return form
    return None
