# from hcss_blog import create_app
from hcss_blog import app
from datetime import datetime, date, timedelta
from hcss_blog.models import Post
import calendar

# app = create_app()

@app.context_processor
def utility_processor():
    posts = Post.query.filter((Post.tags!=None) & (Post.status=='approved')).all()
    all_tags = {}
    for post in posts:
        tags = post.tags.split('#')
        for tag in tags:
            tag = tag.strip().lower()
            if tag != '':
                count = all_tags.get(tag,0)
                all_tags[tag] = count + 1
    sorted_tags = {k: v for k, v in sorted(all_tags.items(), key=lambda item: item[1], reverse=True)}
    return dict(all_tags=list(sorted_tags.keys())[:10] if len(sorted_tags.keys())>10 else sorted_tags.keys())
    # return dict(all_tags=sorted_tags)


@app.context_processor
def utility_processor():
    last_months = []
    time = date.today()

    for i in range(0, 12):
        last_months.append(time.strftime('%B %Y'))
        num_days = calendar.monthrange(time.year, time.month)[1]
        month_len = timedelta(days=num_days)
        time = time - month_len

    return dict(last_months=last_months)

@app.context_processor
def utility_processor():
    posts  = Post.query.filter(Post.post_photo != 'no_picture.jpg').\
                        order_by(Post.date_posted.desc()).all()[:3]
    return dict(latest_posts=posts)

@app.template_filter('time_passed')
def elapsed_time(date):
    # seconds = datetime(2020,9,14) - date
    seconds = datetime.utcnow() - date
    elapsed_time = datetime(1,1,1) + seconds
    if (elapsed_time.year - 1) >= 1:
        return  determine_time('year', elapsed_time.year-1)
    elif (elapsed_time.month - 1) >=1:
        return  determine_time('month', elapsed_time.month-1)
    else:
        return  determine_time('day', elapsed_time.day-1)

def determine_time(time, length):
    if length == 1:
        return str(length) + " "+time+' ago'
    else:
        return str(length) + " "+time+'s ago'

@app.context_processor
def utility_processor():
  def time_passed(date):
      # seconds = datetime(2020,10,13) - date
      seconds = datetime.utcnow() - date
      elapsed_time = datetime(1,1,1) + seconds
      if (elapsed_time.year - 1) >= 1:
          return  str(elapsed_time.year-1) + ' year(s) ago'
      elif (elapsed_time.month - 1) >=1:
          return str(elapsed_time.month-1) + ' month(s) ago'
      else:
          return str(elapsed_time.day-1) + ' day(s) ago'
  return dict(time_passed=time_passed)

if __name__ == '__main__':
    app.run(debug=False)
