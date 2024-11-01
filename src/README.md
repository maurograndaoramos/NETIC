# Para usar um Card

```html
{%include 'components/card.html' with size="small" image="" name="" course="curso" description="descricao" %}
```
Existem 3 tamanhos :
- pequeno : small
- medio : medium
- espaco vazio : grande

# Para usar o fundo de particulas
```html
    {% include 'particle/particle.html' with quantity=20 %}
```

Gerir quantidade : 
- quantity : quantidade de particulas na tela 
- nao coloque mais de 2000

*Particula ja vem na html base
