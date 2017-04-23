import pipy
 
packpath = "classypie"
pipy.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="ClassyPie",
                   changes=["First official version"],
                   description="Python library for classifying/grouping data values.",
                   url="http://github.com/karimbahgat/ClassyPie",
                   keywords="data classification grouping algorithm scheme",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop'],
                   )

pipy.generate_docs(packpath)
#pipy.upload_test(packpath)
#pipy.upload(packpath)

