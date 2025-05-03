import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
import seaborn as sns
import os

# Load data
df = pd.read_csv('data/top-1000-trending-youtube-videos.csv')

# Preview
print("Initial Preview:")
print(df.head())
print("\nColumns:", df.columns)

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')

# Confirm actual columns after cleaning
print("\nNormalized Columns:", df.columns.tolist())

# Drop rows missing key values
df.dropna(subset=['video_views', 'likes'], inplace=True)

# Convert numeric columns with commas to integers
df['video_views'] = df['video_views'].str.replace(',', '').astype(int)
df['likes'] = df['likes'].str.replace(',', '').astype(int)

# Top 10 videos by views
top_10 = df.sort_values('video_views', ascending=False).head(10)

# Output directory and Excel export
os.makedirs('output', exist_ok=True)
with pd.ExcelWriter('output/summary.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Cleaned_Data', index=False)
    top_10.to_excel(writer, sheet_name='Top_10_Viewed', index=False)

print("✅ Excel report saved to output/summary.xlsx")

# Plot: Top 10 videos by views
plt.figure(figsize=(12, 6))
sns.barplot(data=top_10, x='video_views', y='video', palette='viridis')
plt.title('Top 10 Most Viewed YouTube Videos')
plt.xlabel('Views')
plt.ylabel('Video Title')
plt.tight_layout()

# Save the plot
plt.savefig('output/top_10_views_plot.png')
plt.close()

# Category summary
category_summary = df.groupby('category')['video_views'].agg(['count', 'sum']).sort_values(by='sum', ascending=False)
category_summary.reset_index(inplace=True)

# Save to Excel
with pd.ExcelWriter('output/summary.xlsx', engine='openpyxl', mode='a') as writer:
    category_summary.to_excel(writer, sheet_name='Views_By_Category', index=False)

# Create total views by category
category_summary = df.groupby('category')['video_views'].sum().sort_values(ascending=False)

# Plot: Total views by category
plt.figure(figsize=(10, 6))
sns.barplot(x=category_summary.values, y=category_summary.index, palette='coolwarm')
plt.title('Total YouTube Views by Category')
plt.xlabel('Total Views')
plt.ylabel('Category')
plt.tight_layout()

# Save the chart
plt.savefig('output/views_by_category.png')
plt.close()