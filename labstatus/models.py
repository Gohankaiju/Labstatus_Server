from django.db import models
from django.utils import timezone
from django.db.models import Sum

class LabMember(models.Model):
    last_active = models.DateTimeField(null=True, default=timezone.now)
    name = models.CharField(max_length=100)
    is_present = models.BooleanField(default=False)
    
    monthly_total_time = models.FloatField(default=0)
    monthly_entry_count = models.IntegerField(default=0)
    average_daily_time = models.FloatField(default=0)
    
    last_entry_time = models.DateTimeField(null=True, blank=True)
    month_first_entry = models.DateTimeField(null=True, blank=True)

    def handle_entry(self, entry_time):
        entry_time = timezone.make_aware(entry_time)
        self.last_entry_time = entry_time
        self.monthly_entry_count += 1
        if self.month_first_entry is None or self.month_first_entry.month != entry_time.month:
            # 前月の統計をアーカイブに保存
            if self.month_first_entry:
                MonthlyArchive.objects.create(
                    member=self,
                    year=self.month_first_entry.year,
                    month=self.month_first_entry.month,
                    total_time=self.monthly_total_time,
                    entry_count=self.monthly_entry_count,
                    average_daily_time=self.average_daily_time
                )
            # 新しい月の統計を初期化
            self.month_first_entry = entry_time
            self.monthly_total_time = 0
            self.monthly_entry_count = 1
            self.average_daily_time = 0

    def handle_exit(self, exit_time):
        if self.last_entry_time:
            exit_time = timezone.make_aware(exit_time)
            time_spent = exit_time - self.last_entry_time
            self.monthly_total_time += int(time_spent.total_seconds() / 60 / 60)
            self.last_entry_time = None
            
            days_since_first_entry = (exit_time.date() - self.month_first_entry.date()).days + 1
            self.average_daily_time = self.monthly_total_time / days_since_first_entry

    def get_monthly_stats(self, year, month):
        return MonthlyArchive.objects.filter(member=self, year=year, month=month).first()

    def __str__(self):
        return self.name

class MonthlyArchive(models.Model):
    member = models.ForeignKey(LabMember, on_delete=models.CASCADE, related_name='monthly_archives')
    year = models.IntegerField()
    month = models.IntegerField()
    total_time = models.IntegerField()  # 分単位
    entry_count = models.IntegerField()
    average_daily_time = models.FloatField()

    class Meta:
        unique_together = ('member', 'year', 'month')

    def __str__(self):
        return f"{self.member.name} - {self.year}/{self.month}"