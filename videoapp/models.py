from django.conf import settings
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from pilkit.processors import Thumbnail
from .utils import save_frame_from_video
import os

class Video(models.Model):
    title = models.CharField(max_length=50)
    category_choices = (('entertainment','entertainment'),('tech','tech'),('educational','educational'),('random','random'),('news','news'))
    description = models.TextField()
    category = models.CharField(max_length=30, choices=category_choices, default='random')
    # video = models.FileField(upload_to='static/videos', blank=False)
    author = models.CharField(max_length=50, default='admin')
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    # +' ' + str(self.video)


    image_types = ['image/jpeg', 'image/gif', 'image/png']
    video_types = ['video/webm']

    IMAGE = 'I'
    VIDEO = 'V'
    TYPES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    type = models.CharField(max_length=1, choices=TYPES, blank=True)
    video = models.FileField(upload_to='static/video')

    thumbnail_millisecond = models.IntegerField(default=0)
    thumbnail_source_image = models.ImageField(upload_to='static/videos', null=True, blank=True)
    image_thumbnail = ImageSpecField(source='thumbnail_source_image',
                                     processors=[
                                         ResizeToFit(700,
                                                     400,
                                                     mat_color=(230, 230, 230)),
                                     ],
                                     format='JPEG',
                                     options={'quality': 80})

    def _set_type(self):
        # max bytes to read for file type detection
        read_size = 5 * (1024 * 1024)  # 5MB

        # read mime type of file
        from magic import from_buffer
        mime = from_buffer(self.video.read(read_size), mime=True)

        if mime in self.image_types:
            self.type = self.IMAGE
        elif mime in self.video_types:
            self.type = self.VIDEO

    def _set_thumbnail_source_image(self):
        if self.type == self.IMAGE:
            self.thumbnail_source_image = self.video
        elif self.type == self.VIDEO:
            # create thumbnail source file
            image_path = os.path.splitext(self.video.path)[0] + '_thumbnail_src_image.jpg'
            save_frame_from_video(self.video.path, int(self.thumbnail_millisecond), image_path)

            # generate path relative to media root, because this is the version that ImageField accepts
            media_image_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

            self.thumbnail_source_image = media_image_path

    def save(self, *args, **kwargs):
        if self.type == '':
            self._set_type()
        # if there is no source image
        if not bool(self.thumbnail_source_image):
            # we need to save first, for django to generate path for file in "file" field
            super().save(*args, **kwargs)
            self._set_thumbnail_source_image()

        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Video, related_name='comments',on_delete=models.CASCADE,)
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)