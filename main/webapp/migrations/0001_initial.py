# Generated by Django 5.1.7 on 2025-05-21 04:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MetodoHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo', models.CharField(choices=[('biseccion', 'Bisección'), ('secante', 'Secante'), ('newton', 'Newton-Raphson'), ('regla falsa', 'Regla Falsa'), ('lagrange', 'Lagrange'), ('diferencias divididas', 'Divided differences'), ('neville', 'Neville'), ('eliminacion hacia atras', 'Gaussian elimination with back replacement'), ('pivoteo maximo columnas', 'Gaussian elimination with maximum column pivoting'), ('pivoteo escalado columna', 'Gaussian elimination with column-scaled pivoting'), ('factorizacion lu', 'Factorization LU'), ('trapecio', 'Trapecio simple'), ('trapecio compuesto', 'Trapecio compuesto'), ('simpson 1/3', 'Simpson 1/3'), ('simpson 1/3 compuesto', 'Simpson 1/3 compuesto'), ('simpson 3/8', 'Simpson 3/8'), ('simpson 3/8 compuesto', 'Simpson 3/8 compuesto')], max_length=50)),
                ('parametros', models.TextField()),
                ('resultado', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
