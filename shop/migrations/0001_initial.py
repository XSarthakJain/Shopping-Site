# Generated by Django 3.1.3 on 2022-11-16 15:14

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shop.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0016_auto_20221006_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phoneno', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', shop.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('address_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('deliver_country', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=20)),
                ('mobileno', models.CharField(max_length=15)),
                ('pincode', models.CharField(max_length=10)),
                ('flatno', models.CharField(max_length=250)),
                ('area', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeshboardTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_Catelog', models.ImageField(default='media/profile.jpg', upload_to='media')),
                ('product_Name', models.CharField(max_length=50)),
                ('product_OfferPrice', models.IntegerField()),
                ('product_Price', models.IntegerField()),
                ('product_Company', models.CharField(max_length=50)),
                ('product_Category', models.CharField(max_length=50)),
                ('product_desc', models.CharField(max_length=200)),
                ('product_quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('product_Tax_Percent', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateField()),
                ('enddate', models.DateField()),
                ('promocode', models.CharField(max_length=100)),
                ('no_of_user', models.IntegerField()),
                ('min_purchase', models.IntegerField()),
                ('fixed_amount_off', models.IntegerField()),
                ('promocode_desc', models.CharField(default='', max_length=200)),
                ('promocode_provider', models.CharField(default='', max_length=200)),
                ('display_promo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='productComment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productcomment')),
                ('product_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_features',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_feature_Name', models.CharField(max_length=200)),
                ('product_feature_Value', models.CharField(max_length=200)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='Orderitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_status', models.BooleanField(default=False)),
                ('order_date', models.DateField()),
                ('quantity', models.IntegerField(default=1)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('deliveryAddress', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.deliveryaddress')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='Deshboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deshboard_Product_Catelog', models.ImageField(default='media/deshboard/product.jpg', upload_to='media/deshboard')),
                ('deshboard_Product_Name', models.CharField(max_length=50)),
                ('deshboard_Product_Description', models.TextField(blank=True, null=True)),
                ('deshboard_product_URL', models.URLField(max_length=500)),
                ('deshboard', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.deshboardtags')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.products')),
            ],
        ),
    ]
