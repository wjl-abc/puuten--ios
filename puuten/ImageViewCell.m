//
//  ImageViewCell.m
//  WaterFlowViewDemo
//
//  Created by Smallsmall on 12-6-12.
//  Copyright (c) 2012年 activation group. All rights reserved.
//

#import "ImageViewCell.h"


#define TOPMARGIN 8.0f
#define LEFTMARGIN 8.0f

#define IMAGEVIEWBG [UIColor colorWithRed:0.95 green:0.95 blue:0.95 alpha:1.0]

@implementation ImageViewCell
@synthesize delegate;
@synthesize tt=_tt;

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code
    }
    return self;
}

- (void)setTt:(int)tt
{
    _tt = tt;
}


-(id)initWithIdentifier:(NSString *)indentifier
{
	if(self = [super initWithIdentifier:indentifier])
	{
        self.backgroundColor = [UIColor colorWithPatternImage:[UIImage imageNamed:@"concrete_wall_3.png"]];
        //self.backgroundColor = [UIColor colorWithRed:0.90 green:0.92 blue:0.99 alpha:1];
        
        imageView = [[UIImageView alloc] init];
        imageView.backgroundColor = IMAGEVIEWBG;
        [self addSubview:imageView];
        [imageView release];
        imageView.layer.borderWidth = 1;
        imageView.layer.borderColor = [[UIColor colorWithRed:0.85 green:0.85 blue:0.85 alpha:1.0] CGColor];
        
        bsName = [[UILabel alloc] init];
        bsName.font = [UIFont fontWithName:@"Helvetica-Bold" size:10];
        bsName.backgroundColor = [UIColor colorWithRed:1 green:1 blue:1 alpha:1];
        [self addSubview:bsName];
        [bsName release];
        
        avatar = [[UIImageView alloc] init];
        avatar.backgroundColor = [UIColor colorWithRed:1 green:1 blue:1 alpha:1];
        [self addSubview:avatar];
        [avatar release];
        
        name = [[UILabel alloc] init];
        name.font = [UIFont fontWithName:@"Helvetica-Bold" size:10];
        name.backgroundColor = [UIColor colorWithRed:1 green:1 blue:1 alpha:1];
        [self addSubview:name];
        [name release];
        
        info = [[UILabel alloc] init];
        info.font = [UIFont fontWithName:@"Helvetica-Bold" size:10];
        info.numberOfLines = 2;
        [self addSubview:info];
        [info release];
	}
	
	return self;
}

-(void)setImageWithURL:(NSURL *)imageUrl withWB_ID:(int)wb_id withBS:(NSString *)BSinfo withType:(int)Type withDelegate:(id)Delegate{

    [imageView setImageWithURL:imageUrl];
    WB_ID = wb_id;
    bsName.text = BSinfo;
    if (!_tt) {
        bsName.frame = CGRectMake(imageView.frame.origin.x, imageView.frame.origin.y+imageView.frame.size.height, imageView.frame.size.width, 50);
    }
    else
    {
        bsName.frame = CGRectZero;
    }
    type=Type;
    delegate = Delegate;
}

-(void)setImage:(UIImage *)image withWB_ID:(int)wb_id withBS:(NSString *)BSinfo{

    imageView.image = image;
    WB_ID = wb_id;
    bsName.text = BSinfo;
}

-(void)setImageWithURL:(NSURL *)imageUrl
             withWB_ID:(int)wb_id
                withBS:(NSString *)BSinfo
              withType:(int)Type
            withAvatar:(NSURL *)avatarUrl
              withName:(NSString *)Name
              withInfo:(NSString *)Info
          withDelegate:(id)Delegate{
    [imageView setImageWithURL:imageUrl];
    WB_ID = wb_id;
    bsName.text = BSinfo;
    [avatar setImageWithURL:avatarUrl];
    name.text = Name;
    info.text = Info;
    if (!_tt) {
        bsName.frame = CGRectMake(imageView.frame.origin.x, imageView.frame.origin.y+imageView.frame.size.height, imageView.frame.size.width, 12);
        avatar.frame = CGRectMake(imageView.frame.origin.x, imageView.frame.origin.y+imageView.frame.size.height+15, 43, 43);
        name.frame = CGRectMake(imageView.frame.origin.x+45, imageView.frame.origin.y+imageView.frame.size.height+15, imageView.frame.size.width-45, 12);
        info.frame = CGRectMake(imageView.frame.origin.x+45, imageView.frame.origin.y+imageView.frame.size.height+30, imageView.frame.size.width-45, 28);
    }
    else
    {
        bsName.frame = CGRectZero;
    }
    type=Type;
    delegate = Delegate;
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    //[self.delegate imageViewCell:self clickedCell:WB_ID];
    [self.delegate imageViewCell:self clickedCell:WB_ID];
}

//保持图片上下左右有固定间距
-(void)relayoutViews{

    float originX = 0.0f;
    float originY = 0.0f;
    float width = 0.0f;
    float height = 0.0f;
    
    originY = TOPMARGIN;
    height = CGRectGetHeight(self.frame) - TOPMARGIN;
    if (self.indexPath.column == 0) {
        
        originX = LEFTMARGIN;
        width = CGRectGetWidth(self.frame) - LEFTMARGIN - 1/2.0*LEFTMARGIN;
    }else if (self.indexPath.column < self.columnCount - 1){
    
        originX = LEFTMARGIN/2.0;
        width = CGRectGetWidth(self.frame) - LEFTMARGIN;
    }else{
    
        originX = LEFTMARGIN/2.0;
        width = CGRectGetWidth(self.frame) - LEFTMARGIN - 1/2.0*LEFTMARGIN;
    }
    if (self.tt==1) {
        imageView.frame = CGRectMake( originX, originY,width, height);
    }
    else{
        imageView.frame = CGRectMake( originX, originY,width, height-58);
    }
    [super relayoutViews];

}

@end
