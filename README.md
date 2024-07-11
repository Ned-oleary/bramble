This is an integration for Apollo + Hubspot. It lets me throw a list of domains and a list of job titles into Apollo and load all results into Hubspot.

It's equally a toy app written for a little bit of practice as it is something that I find personally useful. I have a bunch of changes I'd like to make at some point, but working on this stopped being fun, so I'll probably not do anything more until I have personal need.

I hacked this together a few minutes at a time while watching Vikings, and it's really not optimized in any way. For instance, I pull all records from Hubspot at the start to prevent duplicates -- which results in a lot of slowness, but I really don't need to do that. I could just handle Hubspot's messages re: failed record creation a little more gracefully. 