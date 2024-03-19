from PIL import Image, ImageDraw, ImageFilter

# - - - - - - - - - - - - - - - - -

template = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template.png')
img_untampered = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_1.jpg').resize((750, 533))
img_tampered_1 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_2.jpg').resize((750, 533)) #(350, 250)     
template.paste(img_untampered, (25, 33))
template.paste(img_tampered_1, (825, 33))
template.save('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template_1_bo.jpg', quality=95)

template = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template.png')
img_untampered = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_1.jpg').resize((750, 533))
img_tampered_1 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_2.jpg').resize((750, 533)) #(350, 250)     
template.paste(img_untampered, (25, 33))
template.paste(img_tampered_1, (825, 33))
template.save('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template_1_p.jpg', quality=95)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

template = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template.png')
img_untampered = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_1.jpg').resize((750, 533))
img_tampered_1 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_2.jpg').resize((350, 250))   
img_tampered_2 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_3.jpg').resize((350, 250))   
img_tampered_3 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_4.jpg').resize((350, 250))   
img_tampered_4 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/bo_5.jpg').resize((350, 250))   
template.paste(img_untampered, (25, 33))
template.paste(img_tampered_1, (825, 33))
template.paste(img_tampered_2, (825, 317))
template.paste(img_tampered_3, (1225, 33))
template.paste(img_tampered_4, (1225, 317))
template.save('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template_4_bo.jpg', quality=95)

template = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template.png')
img_untampered = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_1.jpg').resize((750, 533))
img_tampered_1 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_2.jpg').resize((350, 250))   
img_tampered_2 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_3.jpg').resize((350, 250))   
img_tampered_3 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_4.jpg').resize((350, 250))   
img_tampered_4 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/p_5.jpg').resize((350, 250))   
template.paste(img_untampered, (25, 33))
template.paste(img_tampered_1, (825, 33))
template.paste(img_tampered_2, (825, 317))
template.paste(img_tampered_3, (1225, 33))
template.paste(img_tampered_4, (1225, 317))
template.save('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template_4_p.jpg', quality=95)