//
//  BSHeader.m
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import "BSHeader.h"
#import "Constance.h"
#import "UIImageView+WebCache.h"
#import "ASIHTTPRequest.h"
#import "JMWhenTapped.h"

@implementation BSHeader
@synthesize delegate;
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
    CGRect labelFrame = CGRectMake(80, 10, 400, 20);
    label_test.frame = labelFrame;
    //label_test.text = @"mmmmmm";
    //[self addSubview:label_test];
    UIImageView *image_view_test = [[UIImageView alloc] init];
    CGRect image_view_frame = CGRectMake(0, 0, 50, 50);
    image_view_test.frame = image_view_frame;
    
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/bs_weibo_list/%d/", _bs_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *bsURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:bsURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        label_test.text = [json objectForKey:@"name"];
        NSURL *imageURL = [NSURL URLWithString:[json objectForKey:@"avatar_url"]];
        [image_view_test setImageWithURL:imageURL];
        [self addSubview:label_test];
        [self addSubview:image_view_test];
    }];
    [request setFailedBlock:^{
        
    }];
    
    [request startAsynchronous];
    [image_view_test whenTapped:^{
        [self.delegate bsHeader:self clickedBS:_bs_id];
    }];
    [label_test whenTapped:^{
        [self.delegate bsHeader:self clickedBS:_bs_id];
    }];
     
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