from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Deck, Card
from .forms import DeckCreateForm, CardCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

    
class DeckCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'deck_create.html'
    form_class = DeckCreateForm
    success_url = reverse_lazy('flash_card:deck-list')

    success_message = '"%(title)s" was created successfully.'
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class DeckListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'deck_list.html'
    queryset = Deck.objects.order_by('-updated_at')[:8]


class DeckDetailView(LoginRequiredMixin, DetailView):           # equal to CardListView
    template_name = 'deck_detail.html'      
    model = Deck

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d1 = Deck.objects.get(pk=self.kwargs.get('pk')) 
        context['card_list'] = d1.card_set.all()
        return context

    def get_object(self):
        deck = super().get_object()
        deck.view += 1
        deck.save()
        return deck


class DeckUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'deck_update.html'
    form_class = DeckCreateForm
    success_url = reverse_lazy('flash_card:deck-list')

    success_message = '"%(title)s" was updated successfully.'
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Deck, pk=pk)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class CardUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'card_update.html'
    form_class = CardCreateForm
    model = Card
    pk_url_kwarg = 'id'

    success_message = '"%(title)s" was updated successfully.'
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )

    def get_success_url(self):
        card = get_object_or_404(Card, id=self.kwargs.get('id'))
        return reverse('flash_card:deck-detail', kwargs={'pk': card.deck.pk})


class DeckDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'deck_delete.html'
    model = Deck
    success_url = reverse_lazy('flash_card:deck-list')

    success_message = '"%(title)s" was deleted successfully.'
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )


class CardDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'card_delete.html'
    model = Card
    pk_url_kwarg = 'id'

    def get_success_url(self):
        card = get_object_or_404(Card, id=self.kwargs.get('id'))
        return reverse('flash_card:deck-detail', kwargs={'pk': card.deck.pk})
