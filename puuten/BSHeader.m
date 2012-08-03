//
//  BSHeader.m
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import "BSHeader.h"
#import "ASIHTTPRequest.h"

@implementation BSHeader
@synthesize bs_id = _bs_id;
@synthesize name = _name;
@synthesize avatar_url = _avatar_url;
@synthesize nameLabel = _nameLabel;
@synthesize imageView = _imageView;

- (void)baseInit{
    _nameLabel=nil;
    _name = nil;
    _avatar_url = nil;
    _imageView = nil;
}

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        [self baseInit];
    }
    return self;
}

- (id)initWithCoder:(NSCoder *)aDecoder {
    if ((self = [super initWithCoder:aDecoder])) {
        [self baseInit];
    }
    return self;
}

- (void)layoutSubviews {
    [super layoutSubviews];
    UILabel *label_test =[[UILabel alloc] init];
    CGRect labelFrame = CGRectMake(80, 20, 400, 20);
    label_test.frame = labelFrame;
    label_test.text = self.name;
    [self addSubview:label_test];
    UIImageView *image_view_test = [[UIImageView alloc] init];
    CGRect image_view_frame = CGRectMake(10, 10, 50, 50);
    image_view_test.frame = image_view_frame;
    NSURL *nsURL = [[NSURL alloc] initWithString:self.avatar_url];
    ASIHTTPRequest *request = [ASIHTTPRequest requestWithURL:nsURL];
    [request setCompletionBlock:^{
        UIImage *image = [[UIImage alloc] initWithData:[request responseData]];
        [image_view_test setImage:image];
        [self addSubview:image_view_test];
    }];
    [request setFailedBlock:^{
        NSLog(@"%@", @"ppppp");
    }];
    [request startAsynchronous];
}

- (void)setNameLabel:(UILabel *)nameLabel
{
    _nameLabel = nameLabel;
    
}

- (void)setBs_id:(int)bs_id{
    _bs_id = bs_id;
}

- (void)setImageView:(UIImageView *)imageView{
    _imageView = imageView;
}

- (void)setName:(NSString *)name{
    _name = name;
}

- (void)setAvatar_url:(NSString *)avatar_url
{
    _avatar_url = avatar_url;
}

/*
 - (void)setName:(NSString *)name{
 _name = @"great";
 }
 */

/*
 // Only override drawRect: if you perform custom drawing.
 // An empty implementation adversely affects performance during animation.
 - (void)drawRect:(CGRect)rect
 {
 // Drawing code
 }
 */

@end