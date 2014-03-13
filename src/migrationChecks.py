import database

def check_links(show = "all"):
	
	main_tags = database.get_tags()
	main_random_images = database.get_image_for_every_main_tag()		

	for main_tag in main_tags:
		images = database.get_images_by_tag({'main_tag': main_tag})
					
		#If the main_tag has images in it
		if (len(images) >= 1):
			print("\n" + main_tag + ": " + str( len(images) ) + " Total Images"), 

			#Did the main_tag return at least 1 random image
			try:
				#If no random images are returned there will be no key in 'main_random_images' 
				#And this will fall through to missing a random/carousel image
				main_random_images[main_tag]
				print ("(Good)")

				sub_tags = database.get_sub_tags(main_tag)
				sub_random_images = database.get_image_for_each_sub_tag(main_tag)					
			
				#Now find out if the sub_tags with images each have a carousel image
				for sub_tag in sub_tags:
					sub_images = database.get_images_by_tag({'main_tag': sub_tag[0], 'sub_tag': sub_tag[1]})						

					if len(sub_images) >= 1:							
						print( "\t\t" +  sub_tag[1] +  ": " +  str( len(sub_images)) + " Images"),
						try: 								
							sub_random_images[sub_tag[1]]
							print("(Good)")

							event_tags = database.get_event_tags()							
							event_random_images = database.get_image_for_each_event_tag(sub_tag[1])								
							misc_count = database.get_misc_count_by_tag({'main_tag': sub_tag[0], 'sub_tag': sub_tag[1]})
							misc_random = database.get_image_for_misc_sub_tag(sub_tag[0], sub_tag[1])

							if misc_count >= 1:
								print ( "\t\t\t" + "Misc: " + str(misc_count)  ),
								if len(misc_random) >= 1:
									print("(Good)")
								else:
									print("(Missing Carousel)")


							for event_main_tag, event_sub_tag, event_tag in event_tags:									
								if event_sub_tag == sub_tag[1]:
									event_images = database.get_images_by_tag( {'main_tag': sub_tag[0], 'sub_tag': sub_tag[1], 'event_tag': event_tag} )
									
									if len(event_images) >= 1:
										print ("\t\t\t" + event_tag + ": " + str( len(event_images) ) ),

										try:
											event_random_images[event_tag]
											print("(Good)")
										except:
											print("(Missing Carousel)")
										

						except:
							print("(Missing Carousel)")


			except:
				print ("- Missing Carousel")
								
			
					
if __name__ == "__main__":
	check_links()




