from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from . import models
from produto.models import Produto
from perfil.models import Perfil

# Create your views here.
class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        produto_id = self.request.GET.get('vid')

        if not produto_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        # variacao = get_object_or_404(models.Produto, id=produto_id)

        produto = Produto.objects.filter(id = produto_id).first()

        estoque = produto.estoque
        # produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        # variacao_nome = variacao.nome or ''
        preco_unitario = produto.preco_marketing
        preco_unitario_promocional = produto.preco_marketing_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if produto_id in carrinho:
            quantidade_carrinho = carrinho[produto_id]['quantidade']
            quantidade_carrinho += 1

            if estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = estoque

            carrinho[produto_id]['quantidade'] = quantidade_carrinho
            carrinho[produto_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[produto_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho
        else:
            carrinho[produto_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                # 'variacao_nome': variacao_nome,
                # 'variacao_id': carrinho_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} adicionado ao seu '
            f'carrinho {carrinho[produto_id]["quantidade"]}x.'
        )

        return redirect(http_referer)

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        produto_id = self.request.GET.get('vid')

        if not produto_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if produto_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][produto_id]

        messages.success(
            self.request,
            f'Produto {carrinho["produto_nome"]} '
            f'removido do seu carrinho.'
        )

        del self.request.session['carrinho'][produto_id]
        self.request.session.save()
        return redirect(http_referer)

class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }

        return render(self.request, 'carrinho/resumodacompra.html', contexto)

class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }

        return render(self.request, 'carrinho/lista.html', contexto)