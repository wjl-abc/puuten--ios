//
//  BSHeader.h
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import <UIKit/UIKit.h>
@class BSHeader;
@protocol BSHeaderDelegate <NSObject>

- (void)bSHeader:(BSHeader *)sender
         setName:(NSString *)name_string
   setAvatar_url:(NSString *)avatar_url;
- (void)bsHeader:(BSHeader *)sender
       clickedBS:(int)BS_id;

@end

@interface BSHeader : UIView
@property (assign, nonatomic) int bs_id;
@property (assign, nonatomic) NSString *name;
@property (assign, nonatomic) NSString *avatar_url;
@property (strong, nonatomic) UILabel *nameLabel;
@property (strong, nonatomic) UIImageView *imageView;
@property (nonatomic, weak) id<BSHeaderDelegate> delegate;

@end
