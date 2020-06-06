Custom attribute values in Django form field widgets
====================================================

:slug: django-widget-attrs
:date: 2016-06-11 11:08:24
:category: Coding
:status: published

This has frustrated me for so long.

If you want to use checkboxes in a form in Django, the obvious choice is
BooleanField__. There are times it would be *really* useful to have the value
attribute filled out, but by default, Django just checks for the presence of
the field to decide if it's set or not, so the checkbox's ``value`` attribute
isn't used at all.

.. __: https://docs.djangoproject.com/en/1.8/ref/forms/fields/#booleanfield

There are specific times you *really* want the checkbox widget to have a value,
but it's not at all obvious how you actually do it. Hunting around the
documentation doesn't reveal any way to do it, but if you dig around the code,
there's a way: `Field.widget_attrs()`. It takes a Widget__ instance (so you can
inspect it), and returns a dictionary of attributes to add to the widget.

.. __: https://docs.djangoproject.com/en/1.8/ref/forms/widgets/#django.forms.Widget

For example, if we wanted to ensure that the ``value`` attributes was present
and had the value ``1``, here's what we'd do:

.. code-block:: python

    class BooleanField(forms.BooleanField):

        def widget_attrs(self, widget):
            attrs = super(BooleanField, self).widget_attrs(widget)
            attrs['value'] = '1'
            return attrs

It's frustrating that there's no documentation how to do this.
